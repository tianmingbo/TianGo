package user

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"
	"webook/internal/domain"

	"github.com/redis/go-redis/v9"
)

var ErrKeyNotExist = redis.Nil

type RedisUserCache struct {
	client redis.Cmdable
	expire time.Duration
}

func NewUserRedisCache(client redis.Cmdable) *RedisUserCache {
	return &RedisUserCache{
		client: client,
		expire: time.Minute * 15,
	}
}

func (cache *RedisUserCache) Get(ctx context.Context, id int64) (domain.User, error) {
	key := cache.key(id)
	result, err := cache.client.Get(ctx, key).Result()
	if errors.Is(err, redis.Nil) {
		return domain.User{}, ErrKeyNotExist
	}
	if err != nil {
		return domain.User{}, err
	}
	var user domain.User
	err = json.Unmarshal([]byte(result), &user)
	if err != nil {
		return domain.User{}, err
	}
	return user, nil
}

func (cache *RedisUserCache) Set(ctx context.Context, u domain.User) error {
	data, err := json.Marshal(u)
	if err != nil {
		return err
	}
	return cache.client.Set(ctx, cache.key(u.Id), data, cache.expire).Err()
}

func (cache *RedisUserCache) key(id int64) string {
	return fmt.Sprintf("user:info:%d", id)
}
