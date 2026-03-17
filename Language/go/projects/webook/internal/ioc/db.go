package ioc

import (
	"log"
	"webook/internal/repository/dao"

	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Config struct {
	MySQL MySQL `mapstructure:"mysql"` // 对应嵌套的mysql节点
	Redis Redis `mapstructure:"redis"` // 对应嵌套的redis节点
}

type MySQL struct {
	DSN string `mapstructure:"dsn"` // 主机地址
}
type Redis struct {
	Addr     string `mapstructure:"addr"`     // 主机地址
	Password string `mapstructure:"password"` // 密码
}

func InitDb() *gorm.DB {
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
	dsn := config.MySQL.DSN
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	if err := dao.Init(db); err != nil {
		panic(err)
	}
	return db
}
