package ioc

import (
	"fmt"
	"runtime"
	"webook/internal/repository/dao"
	"webook/pkg/logger"

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

func GetOS() string {
	// runtime.GOOS 返回系统标识：
	// windows / linux / darwin(macOS) / freebsd / openbsd 等
	switch runtime.GOOS {
	case "windows":
		return "Windows"
	case "linux":
		return "Linux"
	case "darwin":
		return "macOS"
	case "freebsd":
		return "FreeBSD"
	case "openbsd":
		return "OpenBSD"
	default:
		return fmt.Sprintf("未知系统: %s", runtime.GOOS)
	}
}
func InitDb(l logger.Logger) *gorm.DB {
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
	dsn := config.MySQL.DSN
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		l.Errorf("数据库连接失败: %v", err)
		panic(err)
	}
	if err := dao.Init(db); err != nil {
		l.Errorf("数据库初始化失败: %v", err)
		panic(err)
	}
	return db
}
