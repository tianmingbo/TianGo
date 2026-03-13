package oauth2

import (
	"context"
	"webook/internal/domain"
)

type Service interface {
	AuthURL(ctx context.Context) (string, error)
	VerifyCode(ctx context.Context, code string, state string) (domain.FeiShuInfo, error)
}
