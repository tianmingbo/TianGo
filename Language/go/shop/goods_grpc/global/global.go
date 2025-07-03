package global

import (
	"gorm.io/gorm"
	"lGo/shop/goods_grpc/config"
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
