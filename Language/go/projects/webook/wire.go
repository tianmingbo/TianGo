//必须包含 go:build wireinject 编译标记
//go:build wireinject
// +build wireinject

package main

import (
	"github.com/gin-gonic/gin"
	"github.com/google/wire"
	"webook/internal/repository"
	"webook/internal/repository/cache"
	"webook/internal/repository/dao"
	"webook/internal/service"
	"webook/internal/web"
	"webook/ioc"
)

// 定义注入器函数（Wire 会生成该函数的实现）
// 函数名：NewUserServiceInjector（自定义）
// 返回值：*UserService（最终要获取的对象）
// 函数体：wire.Build(...) 传入所有需要的 Provider
//func NewUserServiceInjector() *wire2.UserService {
//	// wire.Build 传入所有 Provider 函数，Wire 会分析依赖关系
//	wire.Build(wire2.NewDB, wire2.NewUserService)
//	return nil // 返回 nil 仅为语法占位，Wire 会替换为实际逻辑
//}

// 依赖注入，控制反转
func InitWebUser() *gin.Engine {
	wire.Build(
		ioc.InitDb,
		ioc.InitRedis,

		dao.NewUserDao,

		cache.NewUserCache,
		cache.NewCodeRedisCache,

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
