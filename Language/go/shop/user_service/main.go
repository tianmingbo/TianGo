package main

import (
	"go.uber.org/zap"
	"lGo/shop/user_service/initialize"
)

func main() {
	//初始化文件路径
	initialize.InitFilePath()
	//初始化logger
	initialize.InitLogger()
	zap.S().Debug("start success")
}
