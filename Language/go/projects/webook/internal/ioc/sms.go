package ioc

import (
	"webook/internal/service/sms"
	"webook/internal/service/sms/memory"
	"webook/pkg/logger"
)

func InitSMSService(l logger.Logger) sms.Service {
	return memory.NewService(l.Named("sms"))
}
