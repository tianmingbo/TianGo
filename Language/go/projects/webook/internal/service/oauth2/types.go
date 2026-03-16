package oauth2

import (
	"context"
	"webook/internal/domain"
)

type Service interface {
	AuthURL(ctx context.Context, state string) (string, error)
	// VerifyCode 验证用code换取access_token和user_id
	VerifyCode(ctx context.Context, code string, state string) (domain.FeiShuInfo, error)
}
