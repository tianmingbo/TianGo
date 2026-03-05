package repository

import (
	"context"
	"webook/internal/repository/cache"
	"webook/internal/repository/cache/code"
)

var (
	ErrCodeSendTooMany        = code.ErrCodeSendTooMany
	ErrCodeVerifyTooManyTimes = code.ErrCodeVerifyTooManyTimes
)

type CacheCodeRepository struct {
	cache cache.CodeCache
}

func NewCodeRepository(cache cache.CodeCache) CodeRepository {
	return &CacheCodeRepository{
		cache: cache,
	}
}

func (c *CacheCodeRepository) Store(ctx context.Context, biz, phone, inputCode string) error {
	return c.cache.Set(ctx, biz, phone, inputCode)
}

func (c *CacheCodeRepository) Verify(ctx context.Context, biz, phone, inputCode string) (bool, error) {
	return c.cache.Verify(ctx, biz, phone, inputCode)
}
