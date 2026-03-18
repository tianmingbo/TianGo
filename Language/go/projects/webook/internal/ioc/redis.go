package ioc

import (
	"webook/pkg/logger"

	"github.com/redis/go-redis/v9"
	"github.com/spf13/viper"
)

func InitRedis(l logger.Logger) redis.Cmdable {
	l = l.Named("system")
	v := viper.New()
	if GetOS() == "Windows" {
		v.SetConfigName("dev_remote") // 配置文件名（不带后缀）
	} else {
		v.SetConfigName("dev") // 配置文件名（不带后缀）
	}
	v.SetConfigType("yaml")
	v.AddConfigPath("./config")
	if err := v.ReadInConfig(); err != nil {
		// 区分「文件不存在」和「读取错误」
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			l.Errorf("配置文件未找到")
			panic(err)
		} else {
			l.Errorf("读取配置文件失败: %v", err)
			panic(err)
		}
	}
	var config Config
	err := v.Unmarshal(&config)
	if err != nil {
		l.Errorf("配置反序列化失败: %v", err)
		panic(err)
	}
	return redis.NewClient(&redis.Options{
		Addr:     config.Redis.Addr,
		Password: config.Redis.Password,
		DB:       0,
	})
}
