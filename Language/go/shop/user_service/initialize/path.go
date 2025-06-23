package initialize

import (
	"fmt"
	"lGo/shop/user_service/global"
	"path"
	"runtime"
)

func InitFilePath() {
	basePath := getAbsPath()
	global.FileConfig.ConfigFile = basePath + "/config/config.yaml"
	global.FileConfig.LogFile = basePath + "/logs"
	fmt.Printf("配置文件路径：%s\n", global.FileConfig.ConfigFile)
}

func getAbsPath() string {
	var abPath string
	_, filename, _, ok := runtime.Caller(2)
	if ok {
		abPath = path.Dir(filename)
	}
	return abPath
}
