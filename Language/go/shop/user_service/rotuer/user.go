package router

import (
	"github.com/gin-gonic/gin"
	"lGo/shop/user_service/api"
	"lGo/shop/user_service/middwares"
)

func InitUserRouter(Router *gin.RouterGroup) {
	userRouter := Router.Group("user")
	{
		userRouter.GET("list", middwares.JWTAuthMiddleware(), api.UserList)
		userRouter.POST("login", api.PasswordLogin)
		//userRouter.POST("register", api.Register)
	}
}
