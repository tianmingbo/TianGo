package service

import (
	"context"
	"fmt"
	"math/rand"
	"webook/internal/repository"
	"webook/internal/service/sms"
)

var (
	ErrCodeSendTooMany        = repository.ErrCodeSendTooMany
	ErrCodeVerifyTooManyTimes = repository.ErrCodeVerifyTooManyTimes
)

const codeTplID = "1234"

type CodeService struct {
	repo   *repository.CodeRepository
	smsSvc sms.Service
}

func NewCodeService(repo *repository.CodeRepository, smsSvc sms.Service) *CodeService {
	return &CodeService{
		repo:   repo,
		smsSvc: smsSvc,
	}
}

func (svc *CodeService) Send(ctx context.Context,
	// 区别使用业务
	biz string,
	// 这个码, 谁来管, 谁来生成？
	phone string) error {
	code := svc.generateCode()
	err := svc.repo.Store(ctx, biz, phone, code)
	if err != nil {
		return err
	}
	err = svc.smsSvc.Send(ctx, codeTplID, []string{code}, phone)
	if err != nil {
		return err
	}
	return nil
}

func (svc *CodeService) generateCode() string {
	return fmt.Sprintf("%06d", rand.Intn(1000000))
}

func (svc *CodeService) Verify(ctx context.Context, biz, phone, inputCode string) (bool, error) {
	return svc.repo.Verify(ctx, biz, phone, inputCode)
}
