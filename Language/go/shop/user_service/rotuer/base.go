package router

import (
	"github.com/gin-gonic/gin"
	"lGo/shop/user_service/api"
)

func InitBaseRouter(Router *gin.RouterGroup) {
	baseRouter := Router.Group("base")
	{
		baseRouter.GET("/captcha", api.GetCaptcha)
	}
}
