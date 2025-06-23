package initialize

import (
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"lGo/shop/user_service/rotuer"
)

func InitRouter() *gin.Engine {
	Router := gin.Default()
	userV1 := Router.Group("/user/v1")
	router.InitUserRouter(userV1)
	zap.S().Info("init router success")
	return Router
}
