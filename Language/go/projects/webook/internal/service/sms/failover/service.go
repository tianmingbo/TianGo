package failover

import (
	"context"
	"errors"
	"log"
	"sync/atomic"
	"webook/internal/service/sms"
)

//实现自动故障转移SMS

type SMSService struct {
	svcs []sms.Service //所有服务
	idx  uint64        //当前调用的服务的下标
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

// SendV1 均匀分布流量
func (s *SMSService) SendV1(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	idx := atomic.AddUint64(&s.idx, 1)
	length := uint64(len(s.svcs))
	for i := idx; i < idx+length; i++ {
		svc := s.svcs[idx%length]
		err := svc.Send(ctx, tplId, paramSet, number...)
		switch err {
		case nil:
			return nil
		case context.Canceled, context.DeadlineExceeded:
			return err
		}
		log.Println(err)
	}

	return errors.New("轮询了所有的服务商，但是发送都失败了")
}
