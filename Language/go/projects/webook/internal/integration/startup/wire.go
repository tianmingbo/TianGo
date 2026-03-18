//go:build wireinject
// +build wireinject

//必须包含 go:build wireinject 编译标记

package startup

import (
	"github.com/google/wire"
	"webook/internal/repository"
	"webook/internal/repository/dao"
	"webook/internal/service"
	"webook/internal/web"
)

func InitArticleHandler() *web.ArticleHandler {
	wire.Build(
		//ioc.InitLogger,
		InitDb,
		//ioc.InitRedis,
		service.NewArticleService,
		repository.NewArticleRepository,
		//handler.NewArticleHandler,
		web.NewArticleHandler,
		dao.NewGormArticleDao,
	)
	return nil
}
