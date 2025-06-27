package global

import (
	"gorm.io/gorm"
	"lGo/shop/user_grpc/config"
)

var (
	DB     *gorm.DB
	SECRET string
	Config config.ServerConfig
)

func init() {

	SECRET = "!$%^fgfgjhqw"
}
