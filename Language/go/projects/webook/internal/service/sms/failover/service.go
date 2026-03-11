package failover

import (
	"context"
	"errors"
	"log"
	"webook/internal/service/sms"
)

//实现自动故障转移SMS

type SMSService struct {
	svcs []sms.Service //所有服务
	idx  int64         //当前调用的服务的下标
}

func NewService(svcs []sms.Service) *SMSService {
	return &SMSService{
		svcs: svcs,
	}
}

func (s *SMSService) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	for _, svc := range s.svcs {
		err := svc.Send(ctx, tplId, paramSet, number...)
		if err == nil {
			return nil
		}
		log.Println(err)
	}
	return errors.New("轮询了所有的服务商，但是发送都失败了")
}
