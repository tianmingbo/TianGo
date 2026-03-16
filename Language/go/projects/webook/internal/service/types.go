package service

import (
	"context"
	"webook/internal/domain"
)

type CodeService interface {
	Send(ctx context.Context,
		// 区别使用业务
		biz string,
		// 这个码, 谁来管, 谁来生成？
		phone string) error
	Verify(ctx context.Context, biz, phone, inputCode string) (bool, error)
}

type UserService interface {
	Signup(ctx context.Context, u domain.User) error
	Login(ctx context.Context, email string, password string) (domain.User, error)
	Edit(ctx context.Context, u domain.User) error
	Profile(ctx context.Context) (domain.User, error)
	FindOrCreateByFeiShu(ctx context.Context, feiShuInfo domain.FeiShuInfo) (domain.User, error)
}
