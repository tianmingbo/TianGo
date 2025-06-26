package global

import (
	ut "github.com/go-playground/universal-translator"
	"github.com/go-redis/redis/v8"

	"lGo/shop/user_service/config"
	"lGo/shop/user_service/proto"
)

type Pool interface {
	GetClient() *redis.Client
}

var (
	UserClient proto.UserClient
	Translator ut.Translator
	FileConfig config.FileConfig
	Config     config.Config
	RedisPool  Pool
)
