package ratelimit

import (
	_ "embed"
	"fmt"
	"net/http"
	"webook/pkg/logger"
	"webook/pkg/ratelimit"

	"github.com/gin-gonic/gin"
)

type Builder struct {
	prefix  string
	limiter ratelimit.Limiter
	l       logger.Logger
}

func NewBuilder(limiter ratelimit.Limiter, l logger.Logger) *Builder {
	return &Builder{
		prefix:  "ip-limiter",
		limiter: limiter,
		l:       l,
	}
}

func (b *Builder) Prefix(prefix string) *Builder {
	b.prefix = prefix
	return b
}

func (b *Builder) Build() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		key := fmt.Sprintf("%s:%s", b.prefix, ctx.ClientIP())
		limited, err := b.limiter.Limit(ctx, key)
		if err != nil {
			b.l.Errorf("rate limit check failed, key=%s, err=%v", key, err)
			// 这一步很有意思，就是如果这边出错了
			// 要怎么办？
			ctx.AbortWithStatus(http.StatusInternalServerError)
			return
		}
		if limited {
			b.l.Infof("request limited, key=%s", key)
			ctx.AbortWithStatus(http.StatusTooManyRequests)
			return
		}
		ctx.Next()
	}
}
