package ratelimit

import "context"

type Limiter interface {
	//Limit key是限流对象
	//返回true，触发限流
	Limit(ctx context.Context, key string) (bool, error)
}
