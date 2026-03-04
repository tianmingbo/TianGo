package cache

import (
	"context"
	"webook/internal/domain"
)

type UserCache interface {
	Set(ctx context.Context, u domain.User) error
	Get(ctx context.Context, id int64) (domain.User, error)
}

type CodeCache interface {
	Set(ctx context.Context, biz, phone, inputCode string) error
	Verify(ctx context.Context, biz, phone, inputCode string) (bool, error)
}
