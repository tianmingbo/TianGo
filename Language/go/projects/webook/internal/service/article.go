package service

import (
	"context"
	"webook/internal/domain"
	"webook/internal/repository"
)

type articleService struct {
	repo repository.ArticleRepository
}

func NewArticleService(repo repository.ArticleRepository) ArticleService {
	return &articleService{
		repo: repo,
	}
}

func (s *articleService) Save(ctx context.Context, art domain.Article) (int64, error) {
	return s.repo.Create(ctx, art)
}
