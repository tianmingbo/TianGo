package memory

import (
	"context"
	"webook/pkg/logger"
)

type Service struct {
	l logger.Logger
}

func NewService(l logger.Logger) *Service {
	return &Service{l: l}
}

func (s Service) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	s.l.Infof("mock sms send, tpl=%s, params=%v, numbers=%v", tplId, paramSet, number)
	return nil
}
