package repository

import (
	"context"
	"webook/internal/repository/cache/code"
)

var (
	ErrCodeSendTooMany        = code.ErrCodeSendTooMany
	ErrCodeVerifyTooManyTimes = code.ErrCodeVerifyTooManyTimes
)

type CodeRepository struct {
	cache *code.RedisCodeCache
}

func NewCodeRepository(cache *code.RedisCodeCache) *CodeRepository {
	return &CodeRepository{
		cache: cache,
	}
}

func (c *CodeRepository) Store(ctx context.Context, biz, phone, inputCode string) error {
	return c.cache.Set(ctx, biz, phone, inputCode)
}

func (c *CodeRepository) Verify(ctx context.Context, biz, phone, inputCode string) (bool, error) {
	return c.cache.Verify(ctx, biz, phone, inputCode)
}
