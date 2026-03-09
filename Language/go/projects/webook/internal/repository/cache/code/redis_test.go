package code

import (
	"context"
	"errors"
	"fmt"
	"github.com/redis/go-redis/v9"
	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"
	"testing"
	"webook/internal/repository/cache/redismocks"
)

func TestRedisCodeCache_Set(t *testing.T) {
	keyFunc := func(biz, phone string) string {
		return fmt.Sprintf("phone_code:%s:%s", biz, phone)
	}
	testCases := []struct {
		name      string
		mock      func(ctrl *gomock.Controller) redis.Cmdable
		biz       string
		phone     string
		inputCode string
		wantErr   error
	}{
		{name: "设置成功",
			mock: func(ctrl *gomock.Controller) redis.Cmdable {
				cmd := redis.NewCmd(context.Background())
				cmd.SetVal(int64(0))
				cmd.SetErr(nil)
				client := redismocks.NewMockCmdable(ctrl)
				client.EXPECT().Eval(gomock.Any(), luaSetCode,
					[]string{keyFunc("login", "12345")},
					"123456").Return(cmd)
				return client
			},
			biz:       "login",
			phone:     "12345",
			inputCode: "123456",
			wantErr:   nil,
		},
		{name: "设置失败",
			mock: func(ctrl *gomock.Controller) redis.Cmdable {
				cmd := redis.NewCmd(context.Background())
				cmd.SetVal(int64(0))
				cmd.SetErr(errors.New("err db"))
				client := redismocks.NewMockCmdable(ctrl)
				client.EXPECT().Eval(gomock.Any(), luaSetCode,
					[]string{keyFunc("login", "12345")},
					"123456").Return(cmd)
				return client
			},
			biz:       "login",
			phone:     "12345",
			inputCode: "123456",
			wantErr:   errors.New("err db"),
		},
		{name: "发送太频繁",
			mock: func(ctrl *gomock.Controller) redis.Cmdable {
				cmd := redis.NewCmd(context.Background())
				cmd.SetVal(int64(-1))
				cmd.SetErr(nil)
				client := redismocks.NewMockCmdable(ctrl)
				client.EXPECT().Eval(gomock.Any(), luaSetCode,
					[]string{keyFunc("login", "12345")},
					"123456").Return(cmd)
				return client
			},
			biz:       "login",
			phone:     "12345",
			inputCode: "123456",
			wantErr:   errors.New("发送太频繁"),
		},
		{name: "未知错误",
			mock: func(ctrl *gomock.Controller) redis.Cmdable {
				cmd := redis.NewCmd(context.Background())
				cmd.SetVal(int64(-2))
				cmd.SetErr(nil)
				client := redismocks.NewMockCmdable(ctrl)
				client.EXPECT().Eval(gomock.Any(), luaSetCode,
					[]string{keyFunc("login", "12345")},
					"123456").Return(cmd)
				return client
			},
			biz:       "login",
			phone:     "12345",
			inputCode: "123456",
			wantErr:   ErrUnknownForCode,
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			redisCodeCache := NewRedisCodeCache(tc.mock(ctrl))
			err := redisCodeCache.Set(context.Background(), tc.biz, tc.phone, tc.inputCode)
			assert.Equal(t, tc.wantErr, err)
		})
	}

}
