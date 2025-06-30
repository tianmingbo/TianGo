package initialize

import (
	"errors"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"lGo/shop/user_grpc/global"
	"path"
	"runtime"
)

func getAbsPath() string {
	var abPath string
	_, filename, _, ok := runtime.Caller(2)
	if ok {
		abPath = path.Dir(filename)
	}
	return abPath
}

func InitConfig() {
	viper.SetConfigName("config")
	// 配置文件类型
	viper.SetConfigType("yaml")
	// 配置文件搜索路径
	viper.AddConfigPath(getAbsPath()) // 当前目录

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		var configFileNotFoundError viper.ConfigFileNotFoundError
		if errors.As(err, &configFileNotFoundError) {
			// 配置文件不存在（可选处理）
			zap.S().Infof("配置文件未找到，使用默认值或环境变量")
			return
		}
	}
	if err := viper.Unmarshal(&global.Config); err != nil {
		zap.S().Errorf("配置文件解析失败: %v", err)
		return
	}
	zap.S().Info("配置解析成功")
}
