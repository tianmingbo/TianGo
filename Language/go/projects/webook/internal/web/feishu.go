package web

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"github.com/lithammer/shortuuid"
	"net/http"
	"time"
	"webook/internal/service"
	"webook/internal/service/oauth2"
)

type OAuth2FeiShuHandler struct {
	svc      oauth2.Service
	userSvc  service.UserService
	stateKey []byte
}

func NewOAuth2FeiShuHandler(svc oauth2.Service, userSvc service.UserService) *OAuth2FeiShuHandler {
	return &OAuth2FeiShuHandler{
		svc:      svc,
		userSvc:  userSvc,
		stateKey: []byte("rterdtfgjhkuiygtfyrcgbnk"),
	}
}

func (o *OAuth2FeiShuHandler) RegisterRoutes(server *gin.Engine) {
	g := server.Group("/oauth2/feishu")
	g.GET("/authurl", o.AuthURL)
	g.GET("/callback", o.Callback)
}

type StateClaims struct {
	State string
	jwt.RegisteredClaims
}

func (o *OAuth2FeiShuHandler) AuthURL(context *gin.Context) {
	state := shortuuid.New()
	url, err := o.svc.AuthURL(context, state)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{"message": "构造扫码登录URL失败"})
		return
	}
	claims := &StateClaims{
		State: state,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(60 * time.Second)),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenStr, err := token.SignedString(o.stateKey)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{
			"message": "系统异常",
		})
		return
	}
	//设置cookie
	context.SetCookie("jwt-state", tokenStr, 600, "/oauth2/feishu/callback", "", false, true)
	context.JSON(http.StatusOK, gin.H{"message": "success", "data": url})
}

func (o *OAuth2FeiShuHandler) Callback(context *gin.Context) {
	code := context.Query("code")
	state, err, done := o.verify(context)
	if done {
		return
	}
	fmt.Println("code", code)
	info, err := o.svc.VerifyCode(context, code, state)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{"message": "系统错误"})
		return
	}
	user, err := o.userSvc.FindOrCreateByFeiShu(context, info)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{"message": "系统错误"})
		return
	}
	context.JSON(http.StatusOK, gin.H{"message": "success", "data": user.FeiShuInfo})
}

// verify 校验回调请求中的state参数与cookie中的JWT状态是否一致，返回校验结果及错误信息。
func (o *OAuth2FeiShuHandler) verify(ctx *gin.Context) (string, error, bool) {
	state := ctx.Query("state")
	ck, err := ctx.Cookie("jwt-state")
	if err != nil {
		ctx.JSON(http.StatusOK, gin.H{"message": "登录失败"})
		return "", nil, true
	}

	var s StateClaims
	token, err := jwt.ParseWithClaims(ck, &s, func(token *jwt.Token) (interface{}, error) {
		return o.stateKey, nil
	})
	if err != nil || !token.Valid {
		// 做好监控，防止有人恶意攻击
		// 记录日志
		ctx.JSON(http.StatusOK, gin.H{"message": "登录失败"})
		return "", nil, true
	}

	// 校验 state
	if state != s.State {
		ctx.JSON(http.StatusOK, gin.H{"message": "登录失败"})
		// 做好监控，防止有人恶意攻击
		// 记录日志
		return "", nil, true
	}
	return state, err, false
}
