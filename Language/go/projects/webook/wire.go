//go:build wireinject
// +build wireinject

//必须包含 go:build wireinject 编译标记

package main

import (
	"github.com/gin-gonic/gin"
	"github.com/google/wire"
	"webook/internal/repository"
	"webook/internal/repository/cache/code"
	"webook/internal/repository/cache/user"
	"webook/internal/repository/dao"
	"webook/internal/service"
	"webook/internal/web"
	"webook/ioc"
)

/**
wire.Build()：声明依赖组装规则，是生成注入代码的核心；
wire.NewSet()：分组管理 Provider，提高代码复用性和可读性；
wire.Bind()：绑定接口与实现，解决面向接口编程的依赖注入问题。
*/
// 依赖注入，控制反转
func InitWebUser() *gin.Engine {
	wire.Build(
		ioc.InitDb,
		ioc.InitRedis,

		dao.NewUserDao,

		user.NewUserRedisCache,
		code.NewRedisCodeCache,

		repository.NewUserRepository,
		repository.NewCodeRepository,

		service.NewUserService,
		service.NewCodeService,

		ioc.InitSMSService,

		web.NewUserHandler,
		ioc.InitMiddlewares,
		ioc.InitWebServer,
	)
	return gin.Default()
}
