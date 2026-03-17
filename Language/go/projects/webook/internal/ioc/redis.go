package ioc

import (
	"log"

	"github.com/redis/go-redis/v9"
	"github.com/spf13/viper"
)

func InitRedis() redis.Cmdable {
	v := viper.New()
	v.SetConfigName("dev") // 配置文件名（不带后缀）
	v.SetConfigType("yaml")
	v.AddConfigPath("./config")
	if err := v.ReadInConfig(); err != nil {
		// 区分「文件不存在」和「读取错误」
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Fatal("配置文件未找到")
		} else {
			log.Fatalf("读取配置文件失败: %v", err)
		}
	}
	var config Config
	err := v.Unmarshal(&config)
	if err != nil {
		panic("config err")
	}
	return redis.NewClient(&redis.Options{
		Addr:     config.Redis.Addr,
		Password: config.Redis.Password,
		DB:       0,
	})
}
