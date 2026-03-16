package ioc

import (
	"os"
	"webook/internal/service/oauth2"
)

func InitOAuth2FeiShuService() oauth2.Service {
	appId, ok := os.LookupEnv("FEISHU_APP_ID")
	if !ok {
		appId = "cli_a938dc3865785cbb"

		//panic("FEISHU_APP_ID env variable is not set")
	}
	appKey, ok := os.LookupEnv("FEISHU_APP_SECRET")
	if !ok {
		appKey = "12Vhg5XQ5ESkmiyA70wuIeOICps1vnYO"

		//panic("FEISHU_APP_SECRET env variable is not set")
	}
	return oauth2.NewFeiShuOAuth2Service(appId, appKey)
}
