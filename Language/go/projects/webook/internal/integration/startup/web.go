package startup

import (
	"time"
	"webook/internal/web"
	ijwt "webook/internal/web/jwt"
	"webook/internal/web/middleware"
	"webook/pkg/logger"
	"webook/pkg/ratelimit"

	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"

	//"webook/pkg/middleware/ratelimit"
	limitbuilder "webook/pkg/middleware/ratelimit"
)

func InitWebServer(middlewares []gin.HandlerFunc, userHandler *web.UserHandler, oauthHandler *web.OAuth2FeiShuHandler) *gin.Engine {
	server := gin.Default()
	server.Use(middlewares...)
	userHandler.RegisterRoutes(server)
	oauthHandler.RegisterRoutes(server)
	return server
}

func InitMiddlewares(redisClient redis.Cmdable, jwt ijwt.Jwt, l logger.Logger) []gin.HandlerFunc {
	limiter := ratelimit.NewRedisSlidingWindowLimiter(redisClient, time.Minute, 1000)
	return []gin.HandlerFunc{
		coresHandler(),
		cookieHandler(),
		middleware.GinLoggerMiddleware(l),
		limitbuilder.NewBuilder(limiter, l).Build(),
		loginJWTMiddlewareBuilder(jwt),
	}
}

func coresHandler() gin.HandlerFunc {
	//跨域
	return cors.New(cors.Config{
		AllowOrigins:     []string{"https://foo.com"},
		AllowMethods:     []string{"PUT", "PATCH"},
		AllowHeaders:     []string{"Origin"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowOriginFunc: func(origin string) bool {
			return origin == "https://github.com"
		},
		MaxAge: 12 * time.Hour,
	})
}

func cookieHandler() gin.HandlerFunc {
	store := cookie.NewStore([]byte("secret"))
	return sessions.Sessions("ssid", store)
}

func loginJWTMiddlewareBuilder(jwt ijwt.Jwt) gin.HandlerFunc {
	return middleware.NewLoginMiddleBuilder(jwt).
		IgnorePaths("/users/login").
		IgnorePaths("/users/signup").
		IgnorePaths("/users/login_sms").
		IgnorePaths("/users/login_sms/code/send").
		IgnorePaths("/oauth2/feishu/authurl").
		IgnorePaths("/oauth2/feishu/callback").
		Build()
}
