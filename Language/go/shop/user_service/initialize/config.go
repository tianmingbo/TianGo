package initialize

import (
	"errors"
	"github.com/spf13/viper"
	"go.uber.org/zap"
)

func InitConfig() {
	viper.SetConfigName("config")
	// 配置文件类型
	viper.SetConfigType("yaml")
	// 配置文件搜索路径
	viper.AddConfigPath(".") // 当前目录

	// 环境变量前缀（例如 APP_PORT 对应配置中的 app.port）
	viper.SetEnvPrefix("APP")

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		var configFileNotFoundError viper.ConfigFileNotFoundError
		if errors.As(err, &configFileNotFoundError) {
			// 配置文件不存在（可选处理）
			zap.S().Infof("配置文件未找到，使用默认值或环境变量")
		}
	}
}
