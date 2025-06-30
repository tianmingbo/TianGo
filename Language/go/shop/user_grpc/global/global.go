package global

import (
	"gorm.io/gorm"
	"lGo/shop/user_grpc/config"
)

var (
	DB          *gorm.DB
	SECRET      string
	Config      config.ServerConfig
	NacosConfig config.NacosConfig
)

func init() {

	SECRET = "!$%^fgfgjhqw"
}
