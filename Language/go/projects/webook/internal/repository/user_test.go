package repository

import (
	"context"
	"database/sql"
	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"
	"testing"
	"time"
	"webook/internal/domain"
	"webook/internal/repository/cache"
	cachemocks "webook/internal/repository/cache/mocks"
	"webook/internal/repository/dao"
	daomocks "webook/internal/repository/dao/mocks"
)

func TestCacheUserRepository_FindById(t *testing.T) {
	testUid := int64(11)
	testCases := []struct {
		name string
		mock func(ctrl *gomock.Controller) (dao.UserDao, cache.UserCache)
		ctx  context.Context
		//预期输出
		wantUser domain.User
		wantErr  error
	}{
		{
			name: "缓存未命中,查找数据库成功",
			mock: func(ctrl *gomock.Controller) (dao.UserDao, cache.UserCache) {
				userDao := daomocks.NewMockUserDao(ctrl)
				userCache := cachemocks.NewMockUserCache(ctrl)
				userCache.EXPECT().Get(gomock.Any(), testUid).Return(domain.User{}, ErrKeyNotExist)
				userDao.EXPECT().FindById(gomock.Any()).Return(dao.User{
					ID: testUid,
					Email: sql.NullString{
						String: "123@qq.com",
						Valid:  true,
					},
					Password: "123456",
					Phone: sql.NullString{
						String: "15212345678",
						Valid:  true,
					},
					Ctime: 1,
					Utime: 102,
				}, nil)
				userCache.EXPECT().Set(gomock.Any(), domain.User{
					Id:    testUid,
					Email: "123@qq.com",
					Phone: "15212345678",
				}).Return(nil)
				return userDao, userCache
			},
			ctx: context.WithValue(context.Background(), "UserId", testUid),
			wantUser: domain.User{
				Id:    testUid,
				Email: "123@qq.com",
				Phone: "15212345678",
			},
			wantErr: nil,
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			userDao, UserCache := tc.mock(ctrl)
			userRepo := NewUserRepository(userDao, UserCache)
			user, err := userRepo.FindById(tc.ctx)
			assert.Equal(t, tc.wantErr, err)
			assert.Equal(t, tc.wantUser, user)
			time.Sleep(time.Second)
		})
	}
}
