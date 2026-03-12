package ratelimit

import (
	"context"
	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"
	"testing"
	"webook/internal/service/sms"
	smsMock "webook/internal/service/sms/mocks"
	"webook/pkg/ratelimit"
	ratelimitMock "webook/pkg/ratelimit/mocks"
)

func TestSMSService_Send(t *testing.T) {
	testCases := []struct {
		name    string
		mock    func(ctrl *gomock.Controller) (sms.Service, ratelimit.Limiter)
		wantErr error
	}{
		{
			name: "发送成功",
			mock: func(ctrl *gomock.Controller) (sms.Service, ratelimit.Limiter) {
				limiter := ratelimitMock.NewMockLimiter(ctrl)
				svc := smsMock.NewMockService(ctrl)
				limiter.EXPECT().Limit(gomock.Any(), gomock.Any()).Return(false, nil)
				svc.EXPECT().Send(context.Background(), "123456", []string{}, "15011111111").Return(nil)
				return svc, limiter
			},
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			smsSvc, limit := tc.mock(ctrl)
			limitSvc := NewSMSService(smsSvc, limit, "test")
			err := limitSvc.Send(context.Background(), "123456", []string{}, "15011111111")
			assert.Equal(t, tc.wantErr, err)
		})
	}
}
