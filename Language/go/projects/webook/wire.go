//go:build wireinject
// +build wireinject

//必须包含 go:build wireinject 编译标记

package main

import (
	"webook/internal/ioc"
	"webook/internal/repository"
	"webook/internal/repository/cache/code"
	"webook/internal/repository/cache/user"
	"webook/internal/repository/dao"
	"webook/internal/service"
	"webook/internal/web"
	ijwt "webook/internal/web/jwt"

	"github.com/gin-gonic/gin"
	"github.com/google/wire"
)

/**
wire.Build()：声明依赖组装规则，是生成注入代码的核心；
wire.NewSet()：分组管理 Provider，提高代码复用性和可读性；
wire.Bind()：绑定接口与实现，解决面向接口编程的依赖注入问题。
*/
// 依赖注入，控制反转
func InitWebUser() *gin.Engine {
	wire.Build(
		ioc.InitLogger,
		ioc.InitDb,
		ioc.InitRedis,

		dao.NewUserDao,
		dao.NewGormArticleDao,

		user.NewUserRedisCache,
		code.NewRedisCodeCache,

		repository.NewUserRepository,
		repository.NewCodeRepository,
		repository.NewArticleRepository,

		service.NewUserService,
		service.NewCodeService,
		service.NewArticleService,

		ioc.InitSMSService,
		ioc.InitMiddlewares,
		ioc.InitOAuth2FeiShuService,

		ijwt.NewRedisJwt,
		web.NewUserHandler,
		web.NewArticleHandler,
		web.NewOAuth2FeiShuHandler,

		ioc.InitWebServer,
	)
	return gin.Default()
}
