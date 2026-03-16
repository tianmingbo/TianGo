package middleware

import (
	"net/http"
	ijwt "webook/internal/web/jwt"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

type LoginMiddleBuilder struct {
	paths []string
	ijwt.Jwt
}

func NewLoginMiddleBuilder(jwt ijwt.Jwt) *LoginMiddleBuilder {
	return &LoginMiddleBuilder{
		Jwt: jwt,
	}
}

func (l *LoginMiddleBuilder) IgnorePaths(path string) *LoginMiddleBuilder {
	l.paths = append(l.paths, path)
	return l
}

func (l *LoginMiddleBuilder) Build() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		// 不需要登录校验
		for _, path := range l.paths {
			if ctx.Request.URL.Path == path {
				ctx.Next()
				return
			}
		}
		// 使用 JWT 进行登录校验
		tokenStr := l.ExtractToken(ctx)
		claims := &ijwt.UserClaims{}
		token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
			return []byte("pBMH@cKP65sknQI%ijB2DzhFnvsfiyt*"), nil
		})
		if err != nil {
			ctx.AbortWithStatus(http.StatusUnauthorized)
			return
		}

		if token == nil || !token.Valid || claims.UserId == 0 {
			ctx.AbortWithStatus(http.StatusUnauthorized)
			return
		}

		// 校验 UserAgent
		if claims.UserAgent != ctx.Request.UserAgent() {
			// 严重的安全问题
			// 理论上要加监控
			ctx.AbortWithStatus(http.StatusUnauthorized)
			return
		}

		// 一种降级策略
		//if redis 崩了 {
		//	return
		//}

		// 验证 ssid
		err = l.CheckSession(ctx, claims.Ssid)
		if err != nil {
			// 要么 redis 有问题，要么已经退出登录
			ctx.AbortWithStatus(http.StatusUnauthorized)
			return
		}

		ctx.Set("claims", claims)
		ctx.Set("userId", claims.UserId)
	}
}
