package main

import (
	"flag"
	"go.uber.org/zap"
	"lGo/shop/user_service/global"
	"lGo/shop/user_service/initialize"
)

func main() {
	//Port := flag.Int("port", 8022, "port: 服务端口(release模式下随机获取)")
	//Mode := flag.String("mode", "release", "mode: 服务启动模式 debug 开发模式 / release 服务注册模式")
	flag.Parse()
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
	err := router.Run(":8888")
	if err != nil {
		panic(err)
	}
	zap.S().Debug("start success")
}
