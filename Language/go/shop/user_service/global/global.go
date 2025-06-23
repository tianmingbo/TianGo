package global

import (
	ut "github.com/go-playground/universal-translator"

	"lGo/shop/user_service/config"
	"lGo/shop/user_service/proto"
)

var (
	UserClient proto.UserClient
	Translator ut.Translator
	FileConfig config.FileConfig
	Config     config.Config
)
