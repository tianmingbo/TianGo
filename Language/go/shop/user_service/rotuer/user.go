package router

import (
	"github.com/gin-gonic/gin"
	"lGo/shop/user_service/api"
	"lGo/shop/user_service/middleware"
)

func InitUserRouter(Router *gin.RouterGroup) {
	userRouter := Router.Group("user")
	{
		userRouter.GET("list", middleware.JWTAuthMiddleware(), api.UserList)
		userRouter.POST("login", api.PasswordLogin)
		//userRouter.POST("register", api.Register)
	}
}
