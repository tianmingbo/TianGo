package web

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"webook/internal/domain"
	"webook/internal/service"
	ijwt "webook/internal/web/jwt"
)

type ArticleHandler struct {
	svc service.ArticleService
	//l   logger.Logger
}

func NewArticleHandler(svc service.ArticleService) *ArticleHandler {
	return &ArticleHandler{
		svc: svc,
		//l:   l,
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
		//a.l.Errorf("未发现用户的 session 信息")
		fmt.Println("未发现用户的 session 信息")
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
		//h.l.Error("保存帖子失败", logger.Error(err))
		return
	}
	ctx.JSON(http.StatusOK, gin.H{"message": "OK", "data": id})
}
