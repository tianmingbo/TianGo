package web

import (
	"errors"
	"net/http"
	"time"
	"webook/internal/domain"
	"webook/internal/service"

	"github.com/dlclark/regexp2"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

const (
	emailPattern = `^(?!\.)((?!\.\.)[a-zA-Z0-9\._%+-])+(?<!\.)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
	pwdPattern   = `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&]).{8,20}$`
)

var JwtKey = []byte("your_secret_key") // 实际生产中应从环境变量读取

type UserHandler struct {
	svc           *service.UserService
	emailRegexExp *regexp2.Regexp
	pwdRegexExp   *regexp2.Regexp
}

func NewUserHandler(svc *service.UserService) *UserHandler {
	return &UserHandler{
		svc:           svc,
		emailRegexExp: regexp2.MustCompile(emailPattern, regexp2.None),
		pwdRegexExp:   regexp2.MustCompile(pwdPattern, regexp2.None),
	}
}

func (u *UserHandler) Register(server *gin.Engine) {
	ug := server.Group("users")
	ug.POST("/login", u.LoginJWT)
	ug.POST("/signup", u.Signup)
	ug.POST("/edit", u.Edit)
	ug.GET("/profile", u.Profile)
}

func (u *UserHandler) Login(c *gin.Context) {
	type LoginReq struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}
	var req LoginReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid request",
		})
		return
	}
	user, err := u.svc.Login(c, req.Email, req.Password)
	if errors.Is(err, service.ErrInvalidUserOrEmail) {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid user or email",
		})
		return
	}
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}

	// 这里登录成功了
	sess := sessions.Default(c)
	// 我可以随便设置值了 放在 session 里的值
	sess.Set("UserId", user.Id)
	sess.Save()

	c.JSON(http.StatusOK, gin.H{"message": "ok"})
}

type Claims struct {
	UserID int64 `json:"user_id"`
	jwt.RegisteredClaims
}

// GenerateToken 生成一个 Token
func GenerateToken(userID int64) (string, error) {
	expirationTime := time.Now().Add(24 * time.Hour) // 有效期 24 小时
	claims := &Claims{
		UserID: userID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(JwtKey)
}
func (u *UserHandler) LoginJWT(c *gin.Context) {
	type LoginReq struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}
	var req LoginReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid request",
		})
		return
	}
	user, err := u.svc.Login(c, req.Email, req.Password)
	if errors.Is(err, service.ErrInvalidUserOrEmail) {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid user or email",
		})
		return
	}
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}

	token, err := GenerateToken(user.Id)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
	c.Header("Authorization", "Bearer "+token)
	c.JSON(http.StatusOK, gin.H{"message": "ok"})
}

func (u *UserHandler) Signup(c *gin.Context) {
	type SignUpReq struct {
		Email           string `json:"email" binding:"required"`
		Password        string `json:"password" binding:"required"`
		ConfirmPassword string `json:"confirm_password" binding:"required"`
	}
	var req SignUpReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid request",
		})
		return
	}
	if req.Password != req.ConfirmPassword {
		c.JSON(http.StatusOK, gin.H{
			"message": "password not match",
		})
		return
	}
	isEmail, err := u.emailRegexExp.MatchString(req.Email)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统错误",
		})
		return
	}
	if !isEmail {
		c.JSON(http.StatusOK, gin.H{
			"message": "邮箱格式错误",
		})
		return
	}
	isPwd, err := u.pwdRegexExp.MatchString(req.Password)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统错误",
		})
		return
	}
	if !isPwd {
		c.JSON(http.StatusOK, gin.H{
			"message": "密码格式不符合要求",
		})
		return
	}
	err = u.svc.Signup(c, domain.User{
		Email:    req.Email,
		Password: req.Password,
	})
	if errors.Is(err, service.ErrUserDuplicateEmail) {
		c.JSON(http.StatusOK, gin.H{
			"message": "邮箱冲突",
		})
		return
	}
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "ok"})
}

func (u *UserHandler) Edit(c *gin.Context) {
	type EditReq struct {
		Nickname string `json:"nickname" binding:"omitempty"`
		Birthday string `json:"birthday" binding:"omitempty"`
		AboutMe  string `json:"about_me" binding:"omitempty"`
	}
	var req EditReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid request",
		})
		return
	}
	if len(req.Nickname) > 30 || len(req.AboutMe) > 1024 {
		c.JSON(http.StatusOK, gin.H{
			"message": "参数过长",
		})
	}
	err := u.svc.Edit(c, domain.User{
		Nickname: req.Nickname,
		Birthday: req.Birthday,
		AboutMe:  req.AboutMe,
	})
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "ok"})

}

func (u *UserHandler) Profile(c *gin.Context) {
	user, err := u.svc.Profile(c)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"message": "ok",
		"data":    user,
	})
}
