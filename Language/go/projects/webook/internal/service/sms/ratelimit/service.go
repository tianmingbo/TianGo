// 实现一个带限流的sms服务
package ratelimit

import (
	"context"
	"errors"
	"webook/internal/service/sms"
	"webook/pkg/ratelimit"
)

var errLimited = errors.New("触发限流")

type SMSService struct {
	//装饰器模式，svc是被装饰的对象
	svc   sms.Service
	limit ratelimit.Limiter
	key   string
}

func NewSMSService(service sms.Service, limit ratelimit.Limiter, key string) *SMSService {
	return &SMSService{
		svc:   service,
		limit: limit,
		key:   key,
	}
}

type SMSServiceV1 struct {
	//组合实现
	sms.Service
	limit ratelimit.Limiter
	key   string
}

func (s *SMSService) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	limit, err := s.limit.Limit(ctx, s.key)
	if err != nil {
		return err
	}
	if limit {
		//触发限流
		return errLimited
	}
	return s.svc.Send(ctx, tplId, paramSet, number...)
}
