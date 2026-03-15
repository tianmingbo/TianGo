package web

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"webook/internal/service/oauth2"
)

type OAuth2FeiShuHandler struct {
	svc oauth2.Service
}

func NewOAuth2FeiShuHandler(svc oauth2.Service) *OAuth2FeiShuHandler {
	return &OAuth2FeiShuHandler{
		svc: svc,
	}
}

func (o *OAuth2FeiShuHandler) RegisterRoutes(server *gin.Engine) {
	g := server.Group("/oauth2/feishu")
	g.GET("/authurl", o.AuthURL)
	g.GET("/callback", o.Callback)
}

func (o *OAuth2FeiShuHandler) AuthURL(context *gin.Context) {
	url, err := o.svc.AuthURL(context)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{"message": "构造扫码登录URL失败"})
		return
	}
	context.JSON(http.StatusOK, gin.H{"message": "success", "data": url})
}

func (o *OAuth2FeiShuHandler) Callback(context *gin.Context) {
	code := context.Query("code")
	state := context.Query("state")
	fmt.Println("code", code)
	info, err := o.svc.VerifyCode(context, code, state)
	if err != nil {
		context.JSON(http.StatusOK, gin.H{"message": "系统错误"})
		return
	}
	context.JSON(http.StatusOK, gin.H{"message": "success", "data": info})
}
