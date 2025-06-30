package main

import (
	"fmt"
	uuid "github.com/satori/go.uuid"
	"go.uber.org/zap"
	"lGo/shop/user_service/global"
	"lGo/shop/user_service/initialize"
	"lGo/shop/user_service/middleware"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	//初始化文件路径
	initialize.InitFilePath()
	//初始化logger
	initialize.InitLogger()
	//初始化翻译器
	initialize.InitTranslator("zh")
	//初始化验证器
	initialize.InitValidator()
	//加载配置
	initialize.InitConfig()
	//
	initialize.InitGrpcClient()

	initialize.InitRedisPool(global.Config.RedisConfig)

	router := initialize.InitRouter()

	go func() {
		zap.S().Infof("启动服务器, 端口： %d", global.Config.Server.Port)
		err := router.Run(fmt.Sprintf("0.0.0.0:%d", global.Config.Server.Port))
		if err != nil {
			panic(err)
		}
		zap.S().Debug("start success")
	}()

	//服务注册
	addr := fmt.Sprintf("%s:%d", global.Config.ConsulInfo.Host, global.Config.ConsulInfo.Port)
	registerClient, _ := middleware.NewConsulService(addr)
	serviceId := fmt.Sprintf("%s", uuid.NewV4())
	err := registerClient.RegisterService(serviceId, global.Config.Server.Name, global.Config.Server.Host, global.Config.Server.Port, global.Config.Server.Tags)
	if err != nil {
		zap.S().Panic("服务注册失败:", err.Error())
	}

	//接收终止信号
	quit := make(chan os.Signal)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	if err = registerClient.DeregisterService(serviceId); err != nil {
		zap.S().Info("注销失败:", err.Error())
	} else {
		zap.S().Info("注销成功:")
	}
}
