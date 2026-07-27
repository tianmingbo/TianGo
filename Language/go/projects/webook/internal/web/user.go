package web

import (
	"errors"
	"net/http"
	"webook/internal/domain"

	"webook/internal/service"
	ijwt "webook/internal/web/jwt"
	"webook/pkg/logger"

	"github.com/dlclark/regexp2"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

const (
	emailPattern = `^(?!\.)((?!\.\.)[a-zA-Z0-9\._%+-])+(?<!\.)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
	pwdPattern   = `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&]).{8,20}$`
)

type UserHandler struct {
	svc           service.UserService
	codeSvc       service.CodeService
	emailRegexExp *regexp2.Regexp
	pwdRegexExp   *regexp2.Regexp
	l             logger.Logger
	ijwt.Jwt
}

func NewUserHandler(svc service.UserService, codeSvc service.CodeService, jwt ijwt.Jwt, l logger.Logger) *UserHandler {
	return &UserHandler{
		svc:           svc,
		codeSvc:       codeSvc,
		emailRegexExp: regexp2.MustCompile(emailPattern, regexp2.None),
		pwdRegexExp:   regexp2.MustCompile(pwdPattern, regexp2.None),
		Jwt:           jwt,
		l:             l,
	}
}

func (u *UserHandler) RegisterRoutes(server *gin.Engine) {
	ug := server.Group("users")
	ug.POST("/login", u.LoginJWT)
	ug.POST("/signup", u.Signup)
	ug.POST("/edit", u.Edit)
	ug.GET("/profile", u.Profile)
	ug.POST("/login_sms/code/send", u.SendLoginSMSCode)
	ug.POST("/login_sms", u.LoginSMS)
	ug.POST("/refresh_token", u.RefreshToken)
	ug.POST("/logout", u.LogoutJWT)

}

func (h *UserHandler) LogoutJWT(ctx *gin.Context) {
	err := h.ClearToken(ctx)
	if err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"message": "退出登录失败",
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "logout"})
	return
}

// RefreshToken 刷新 JWT Token
// 该函数用于通过 refresh token 获取新的 access token，实现令牌的无感知刷新
// 参数:
//   - c: gin.Context，HTTP 请求上下文，包含请求信息和响应对象
//
// 处理流程:
//  1. 从请求中提取 refresh token
//  2. 解析并验证 refresh token 的有效性
//  3. 检查 session 是否仍然有效
//  4. 设置新的 JWT token
//
// 返回值:
//   - 成功时返回 HTTP 200 状态码和成功消息
//   - 失败时返回 HTTP 401 未授权状态码
func (u *UserHandler) RefreshToken(c *gin.Context) {
	// 从请求上下文中提取 refresh token
	refreshToken := u.ExtractToken(c)
	var rc ijwt.RefreshClaims
	// 解析 refresh token 并验证其签名和有效性
	token, err := jwt.ParseWithClaims(refreshToken, &rc, func(token *jwt.Token) (interface{}, error) {
		return ijwt.RefreshTokenKey, nil
	})
	if err != nil || !token.Valid {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}

	// 检查用户 session 是否有效，验证登录状态
	err = u.CheckSession(c, rc.Ssid)
	if err != nil {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}

	// 为用户生成并设置新的 JWT token
	err = u.SetJWTToken(c, rc.UserId, rc.Ssid)
	if err != nil {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "refresh token successfully"})
}

func (u *UserHandler) LoginSMS(c *gin.Context) {
	type Req struct {
		Phone string `json:"phone" binding:"required"`
		Code  string `json:"code" binding:"required"`
	}
	var req Req
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"message": "invalid request"})
		return
	}
	ok, err := u.codeSvc.Verify(c, "login", req.Phone, req.Code)
	if errors.Is(err, service.ErrCodeVerifyTooManyTimes) {
		c.JSON(http.StatusUnauthorized, gin.H{"message": "verify too many times"})
		return
	}
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": "系统异常"})
		return
	}
	if !ok {
		c.JSON(http.StatusOK, gin.H{"message": "验证码错误"})
		return
	}

	//user, err := u.svc.FindOrCreate(c, req.Phone)
	//if err != nil {
	//	c.JSON(http.StatusOK,gin.H{"message": "系统错误"})
	//	return
	//}
	//
	//if err = u.SetLoginToken(c, user.Id); err != nil {
	//	c.JSON(http.StatusOK,gin.H{"message": "系统错误"})
	//	return
	//}

	c.JSON(http.StatusOK, gin.H{"message": "验证码校验成功"})
}

func (u *UserHandler) SendLoginSMSCode(c *gin.Context) {
	type Req struct {
		Phone string `json:"phone" binding:"required"`
	}
	var req Req
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"message": "invalid request",
		})
		return
	}
	err := u.codeSvc.Send(c, "login", req.Phone)
	if errors.Is(err, service.ErrCodeSendTooMany) {
		c.JSON(http.StatusOK, gin.H{
			"message": "send too many",
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
		u.l.Error("invalid user or email", "email", req.Email)

		return
	}
	if err != nil {
		u.l.Error("login failed", "email", req.Email, "error", err)
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}

	err = u.SetLoginToken(c, user.Id)
	if err != nil {
		u.l.Error("set login token failed", "user_id", user.Id, "error", err)
		c.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
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
