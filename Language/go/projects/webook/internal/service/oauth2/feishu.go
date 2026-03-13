package oauth2

import (
	"context"
	"fmt"
	"github.com/lithammer/shortuuid"
	"net/url"
	"webook/internal/domain"
)

var (
	redirectURL = url.PathEscape("https://tmb.com/oauth2/wechat/callbak")
)

type FeiShuOAuth2Service struct {
	appId  string
	secret string
	scope  string
}

func NewFeiShuOAuth2Service(appId string, secret string) *FeiShuOAuth2Service {
	return &FeiShuOAuth2Service{appId: appId, secret: secret, scope: "user:info.basic"}
}

func (f *FeiShuOAuth2Service) AuthURL(ctx context.Context) (string, error) {
	const urlPattern = "https://open.feishu.cn/open-apis/authen/v1/index?app_id=%s&redirect_uri=%sscope=%s&response_type=code&state=%s"
	state := shortuuid.New()
	// 使用生成的state值构建URL
	return fmt.Sprintf(urlPattern, f.appId, redirectURL, f.scope, state), nil
}

func (f *FeiShuOAuth2Service) VerifyCode(ctx context.Context, code string, state string) (domain.FeiShuInfo, error) {
	//TODO implement me
	panic("implement me")
}
