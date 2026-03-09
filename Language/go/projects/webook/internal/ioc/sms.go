package ioc

import (
	"webook/internal/service/sms"
	"webook/internal/service/sms/memory"
)

func InitSMSService() sms.Service {
	return memory.NewService()
}
