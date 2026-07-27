package ioc

import (
	"webook/pkg/logger"
)

func InitLogger() logger.Logger {
	appLog, err := logger.NewLogger("./logs/app.log")
	if err != nil {
		panic(err)
	}
	return appLog
}
