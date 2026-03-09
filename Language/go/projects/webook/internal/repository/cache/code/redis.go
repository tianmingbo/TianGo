package code

import (
	"context"
	_ "embed"
	"errors"
	"fmt"
	"github.com/redis/go-redis/v9"
	"webook/internal/repository/cache"
)

var (
	ErrCodeSendTooMany        = errors.New("发送太频繁")
	ErrCodeVerifyTooManyTimes = errors.New("验证次数太多")
	ErrUnknownForCode         = errors.New("我不知道哪错了")
)

// 编译器在编译的时候，把 set_code 里面的代码放进来
//
//go:embed lua/set_code.lua
var luaSetCode string

//go:embed lua/verify_code.lua
var luaVerifyCode string

type RedisCodeCache struct {
	client redis.Cmdable
}

func NewRedisCodeCache(client redis.Cmdable) cache.CodeCache {
	//接收者是*RedisCodeCache（指针类型），因此*RedisCodeCache类型 “自动实现” 了CodeCache接口
	return &RedisCodeCache{client: client}
}

func (c *RedisCodeCache) Set(ctx context.Context, biz, phone, inputCode string) error {
	res, err := c.client.Eval(
		ctx,
		luaSetCode,
		[]string{c.key(biz, phone)}, // KEYS[1] = phone_code:
		inputCode,                   // ARGV[1] = inputCode
	).Int()
	if err != nil {
		return err
	}
	switch res {
	case 0:
		return nil
	case -1:
		return ErrCodeSendTooMany
	default:
		return ErrUnknownForCode
	}
}

func (c *RedisCodeCache) key(biz, phone string) string {
	return fmt.Sprintf("phone_code:%s:%s", biz, phone)
}

func (c *RedisCodeCache) Verify(ctx context.Context, biz, phone, inputCode string) (bool, error) {
	res, err := c.client.Eval(
		ctx,
		luaVerifyCode,
		[]string{c.key(biz, phone)}, // KEYS[1] = phone_code:
		inputCode,                   // ARGV[1] = inputCode
	).Int()
	if err != nil {
		return false, err
	}
	switch res {
	case 0:
		return true, nil
	case -1:
		return false, ErrCodeVerifyTooManyTimes
	default:
		return false, ErrUnknownForCode
	}
}
