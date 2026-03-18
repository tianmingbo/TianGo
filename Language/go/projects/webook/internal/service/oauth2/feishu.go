package oauth2

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"webook/internal/domain"
	"webook/pkg/logger"
)

var (
	redirectURL = url.PathEscape("https://tmb.com/oauth2/feishu/callback")
)

type FeiShuOAuth2Service struct {
	appId  string
	secret string
	scope  string
	l      logger.Logger
}

func NewFeiShuOAuth2Service(appId string, secret string, l logger.Logger) *FeiShuOAuth2Service {
	return &FeiShuOAuth2Service{appId: appId, secret: secret, scope: "user:info.basic", l: l}
}

func (f *FeiShuOAuth2Service) AuthURL(ctx context.Context, state string) (string, error) {
	const urlPattern = "https://open.feishu.cn/open-apis/authen/v1/index?app_id=%s&redirect_uri=%s&scope=%s&response_type=code&state=%s"
	// 使用生成的state值构建URL
	sprintf := fmt.Sprintf(urlPattern, f.appId, redirectURL, f.scope, state)
	f.l.Infof("generated feishu oauth url, state=%s", state)
	return sprintf, nil
}

type Response struct {
	Code int64  `json:"code"`
	Msg  string `json:"msg"`
	Data Data   `json:"data"` // 只保留需要的Data字段
}

type Data struct {
	AccessToken  string `json:"access_token"`
	ExpiresIn    int    `json:"expires_in"`
	RefreshToken string `json:"refresh_token"`

	OpenId  string `json:"open_id"`
	UnionId string `json:"union_id"`
}

type TokenReq struct {
	AppId     string `json:"app_id"`
	Secret    string `json:"app_secret"`
	Code      string `json:"code"`
	GrantType string `json:"grant_type"`
}

func (f *FeiShuOAuth2Service) VerifyCode(ctx context.Context, code string, state string) (domain.FeiShuInfo, error) {
	const tokenUrl = "https://open.feishu.cn/open-apis/authen/v1/access_token"
	reqData := TokenReq{
		AppId:     f.appId,
		Secret:    f.secret,
		Code:      code,
		GrantType: "authorization_code",
	}
	jsonData, err := json.Marshal(reqData)
	if err != nil {
		f.l.Errorf("marshal feishu token request failed: %v", err)
		return domain.FeiShuInfo{}, err
	}
	resp, err := http.Post(tokenUrl, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return domain.FeiShuInfo{}, err
	}
	// 4. 读取并输出响应
	//buf := new(bytes.Buffer)
	//_, err = buf.ReadFrom(resp.Body)
	//if err != nil {
	//	fmt.Printf("读取响应失败: %v\n", err)
	//	return domain.FeiShuInfo{}, err
	//}
	//fmt.Printf("响应状态码: %d\n", resp.StatusCode)
	//fmt.Printf("响应内容:\n%s\n", buf.String())
	decoder := json.NewDecoder(resp.Body)
	var res Response
	err = decoder.Decode(&res)
	if err != nil {
		return domain.FeiShuInfo{}, err
	}
	if res.Code != 0 {
		return domain.FeiShuInfo{}, fmt.Errorf("feishu return err:%d, msg:%s", res.Code, res.Msg)
	}
	return domain.FeiShuInfo{
		OpenId:  res.Data.OpenId,
		UnionId: res.Data.UnionId,
	}, nil
}
