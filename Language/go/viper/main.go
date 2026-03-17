package main

import (
	"fmt"
	"github.com/spf13/viper"
	"log"
)

func main() {
	// 1. 初始化 Viper 实例
	v := viper.New()

	// 2. 配置文件相关设置
	v.SetConfigName("app")     // 配置文件名（不带后缀）
	v.SetConfigType("yaml")    // 配置文件格式（yaml/json/toml/ini 等）
	v.AddConfigPath("./viper") // 配置文件所在目录（可添加多个，按顺序查找）
	v.AddConfigPath(".")       // 备用查找目录（当前目录）

	// 3. 读取配置文件
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
		return
	}
	fmt.Println(config)
}
