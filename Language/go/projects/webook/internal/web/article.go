package web

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"webook/internal/domain"
	"webook/internal/service"
	ijwt "webook/internal/web/jwt"
	"webook/pkg/logger"
)

type ArticleHandler struct {
	svc service.ArticleService
	l   logger.Logger
}

func NewArticleHandler(svc service.ArticleService, l logger.Logger) *ArticleHandler {
	return &ArticleHandler{
		svc: svc,
		l:   l,
	}
}

func (a *ArticleHandler) RegisterRoutes(server *gin.Engine) {
	ug := server.Group("/articles")
	ug.POST("/edit", a.Edit)
}

func (a *ArticleHandler) Edit(ctx *gin.Context) {
	type Req struct {
		Title   string `json:"title"`
		Content string `json:"content"`
	}
	var req Req
	err := ctx.ShouldBind(&req)
	if err != nil {
		ctx.JSON(http.StatusOK, gin.H{"message": "参数错误"})
		return
	}
	c, _ := ctx.Get("claims")
	claims, ok := c.(*ijwt.UserClaims)
	if !ok {
		ctx.JSON(http.StatusOK, gin.H{"message": "系统错误"})
		a.l.Error("missing claims in context when edit article")
		return
	}
	id, err := a.svc.Save(ctx, domain.Article{
		Title:   req.Title,
		Content: req.Content,
		Author: domain.Author{
			Id: claims.UserId,
		},
	})
	if err != nil {
		ctx.JSON(http.StatusOK, gin.H{"message": "系统错误"})
		a.l.Error("save article failed", "author_id", claims.UserId, "error", err)
		return
	}
	ctx.JSON(http.StatusOK, gin.H{"message": "OK", "data": id})
}
