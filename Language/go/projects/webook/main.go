package main

import (
	"time"
	"webook/internal/repository"
	"webook/internal/repository/cache"
	"webook/internal/repository/dao"
	"webook/internal/service"
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

	server := initWebServer()

	user := initUser(db)
	user.Register(server)

	server.Run(":28080")
}

func initWebServer() *gin.Engine {
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

	cmd := redis.NewClient(&redis.Options{
		Addr:     "localhost:6389",
		Password: "tian666",
		DB:       0,
	})
	server.Use(ratelimit.NewBuilder(cmd, time.Minute, 10).Build())

	server.Use(middleware.NewLoginMiddleBuilder().
		IgnorePaths("/users/login").
		IgnorePaths("/users/signup").
		Build())
	return server
}

func initDb() *gorm.DB {
	dsn := "root:123456@tcp(127.0.0.1:3306)/webook"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	if err := dao.Init(db); err != nil {
		panic(err)
	}
	return db
}

func initUser(db *gorm.DB) *web.UserHandler {
	ud := dao.NewUserDao(db)
	repo := repository.NewUserRepository(ud, &cache.UserCache{})
	svc := service.NewUserService(repo)
	return web.NewUserHandler(svc)
}
