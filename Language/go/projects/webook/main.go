package main

import (
	"time"
	"webook/config"
	"webook/internal/repository"
	"webook/internal/repository/cache"
	"webook/internal/repository/dao"
	"webook/internal/service"
	"webook/internal/service/sms/memory"
	"webook/internal/web"
	"webook/internal/web/middleware"
	"webook/pkg/middleware/ratelimit"

	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func main() {
	db := initDb()
	rdb := initRedis()
	server := initWebServer(rdb)

	user := initUser(db, rdb)
	user.Register(server)

	server.Run(":28080")
}

func initWebServer(rdb redis.Cmdable) *gin.Engine {
	server := gin.Default()
	//跨域
	server.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"https://foo.com"},
		AllowMethods:     []string{"PUT", "PATCH"},
		AllowHeaders:     []string{"Origin"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowOriginFunc: func(origin string) bool {
			return origin == "https://github.com"
		},
		MaxAge: 12 * time.Hour,
	}))

	store := cookie.NewStore([]byte("secret"))
	server.Use(sessions.Sessions("ssid", store))

	server.Use(ratelimit.NewBuilder(rdb, time.Minute, 10).Build())

	server.Use(middleware.NewLoginMiddleBuilder().
		IgnorePaths("/users/login").
		IgnorePaths("/users/signup").
		IgnorePaths("/users/login_sms/code/send").
		IgnorePaths("/users/login_sms").
		Build())
	return server
}

func initDb() *gorm.DB {
	dsn := config.Config.DB.DSN
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	if err := dao.Init(db); err != nil {
		panic(err)
	}
	return db
}
func initRedis() redis.Cmdable {
	return redis.NewClient(&redis.Options{
		Addr:     config.Config.Redis.Addr,
		Password: config.Config.Redis.Password,
		DB:       0,
	})
}

func initUser(db *gorm.DB, rdb redis.Cmdable) *web.UserHandler {
	ud := dao.NewUserDao(db)
	repo := repository.NewUserRepository(ud, &cache.UserCache{})
	svc := service.NewUserService(repo)

	codeCache := cache.NewCodeCache(rdb)
	codeRepo := repository.NewCodeRepository(codeCache)
	smsSvc := memory.NewService()
	codeSvc := service.NewCodeService(codeRepo, smsSvc)

	return web.NewUserHandler(svc, codeSvc)
}
