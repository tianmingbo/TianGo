package tencent

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"

	"github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common"
	tencentError "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common/errors"
	sms "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/sms/v20210111" // 引入sms
)

type Service struct {
	client    *sms.Client
	appId     string
	signature string
}

func newService(client *sms.Client, appId, signature string) *Service {
	return &Service{
		client:    client,
		appId:     appId,
		signature: signature,
	}
}

func (s Service) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	request := sms.NewSendSmsRequest()
	request.SetContext(ctx)
	request.SmsSdkAppId = common.StringPtr(s.appId)
	request.SignName = common.StringPtr(s.signature)
	request.TemplateId = common.StringPtr(tplId)
	request.TemplateParamSet = common.StringPtrs(paramSet)

	request.PhoneNumberSet = common.StringPtrs(number)
	response, err := s.client.SendSms(request)
	// 处理异常
	var tencentCloudSDKError *tencentError.TencentCloudSDKError
	if errors.As(err, &tencentCloudSDKError) {
		fmt.Printf("An API error has returned: %s", err)
		return errors.New(err.Error())
	}
	if err != nil {
		return err
	}
	b, _ := json.Marshal(response.Response)
	fmt.Printf("%s", b)
	return nil
}
