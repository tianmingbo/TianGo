package initialize

import (
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"lGo/shop/user_service/rotuer"
)

func health(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}

func InitRouter() *gin.Engine {
	Router := gin.Default()
	Router.GET("/health", health)
	userV1 := Router.Group("/user/v1")
	router.InitUserRouter(userV1)
	router.InitBaseRouter(userV1)
	zap.S().Info("init router success")
	return Router
}
