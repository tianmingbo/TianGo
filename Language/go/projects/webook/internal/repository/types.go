package repository

import (
	"context"
	"webook/internal/domain"
)

type CodeRepository interface {
	Store(ctx context.Context, biz, phone, inputCode string) error
	Verify(ctx context.Context, biz, phone, inputCode string) (bool, error)
}

type UserRepository interface {
	CreateUser(ctx context.Context, u domain.User) error
	FindByEmail(ctx context.Context, email string) (domain.User, error)
	UpdateById(ctx context.Context, u domain.User) error
	FindById(ctx context.Context) (domain.User, error)
	FindByFeiShu(ctx context.Context, unionId string) (domain.User, error)
}
