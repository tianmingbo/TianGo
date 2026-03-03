package repository

import (
	"context"
	"webook/internal/repository/cache"
)

var (
	ErrCodeSendTooMany        = cache.ErrCodeSendTooMany
	ErrCodeVerifyTooManyTimes = cache.ErrCodeVerifyTooManyTimes
)

type CodeRepository struct {
	cache *cache.CodeRedisCache
}

func NewCodeRepository(cache *cache.CodeRedisCache) *CodeRepository {
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
