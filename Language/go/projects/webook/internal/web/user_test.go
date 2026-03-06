package web

import (
	"bytes"
	"encoding/json"
	"errors"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"go.uber.org/mock/gomock"
	"net/http"
	"net/http/httptest"
	"testing"
	"webook/internal/domain"
	"webook/internal/service"
	svcmocks "webook/internal/service/mocks"
)

func TestUserHandler_Signup(t *testing.T) {
	testCases := []struct {
		name       string
		mock       func(ctrl *gomock.Controller) (service.UserService, service.CodeService)
		reqBuilder func(t *testing.T) *http.Request //预期输入
		//预期输出
		wantCode int
		wantBody string
	}{
		{
			name: "注册成功",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				// 隐含规则：该方法必须被调用 1 次（不调用/多调用都会测试失败）
				userSvc.EXPECT().Signup(gomock.Any(), domain.User{
					Email:    "123@qq.com",
					Password: "Hello#world123",
				}).Return(nil)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123@qq.com",
					"password":         "Hello#world123",
					"confirm_password": "Hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "ok",
		},
		{
			name: "bind error",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":    "123@qq.com",
					"password": "Hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "invalid request",
		},
		{
			name: "密码不一致",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123@qq.com",
					"password":         "Hello#world123",
					"confirm_password": "hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "password not match",
		},
		{
			name: "邮箱格式错误",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123",
					"password":         "Hello#world123",
					"confirm_password": "Hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "邮箱格式错误",
		},
		{
			name: "密码格式不符合要求",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123@qq.com",
					"password":         "hello#world123",
					"confirm_password": "hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "密码格式不符合要求",
		},
		{
			name: "邮箱冲突",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				// 隐含规则：该方法必须被调用 1 次（不调用/多调用都会测试失败）
				userSvc.EXPECT().Signup(gomock.Any(), domain.User{
					Email:    "123@qq.com",
					Password: "Hello#world123",
				}).Return(service.ErrUserDuplicateEmail)
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123@qq.com",
					"password":         "Hello#world123",
					"confirm_password": "Hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "邮箱冲突",
		},
		{
			name: "系统异常",
			mock: func(ctrl *gomock.Controller) (service.UserService, service.CodeService) {
				userSvc := svcmocks.NewMockUserService(ctrl)
				// 隐含规则：该方法必须被调用 1 次（不调用/多调用都会测试失败）
				userSvc.EXPECT().Signup(gomock.Any(), domain.User{
					Email:    "123@qq.com",
					Password: "Hello#world123",
				}).Return(errors.New("random err"))
				codeSvc := svcmocks.NewMockCodeService(ctrl)
				return userSvc, codeSvc
			},
			reqBuilder: func(t *testing.T) *http.Request {
				reqJSON, err := json.Marshal(map[string]string{
					"email":            "123@qq.com",
					"password":         "Hello#world123",
					"confirm_password": "Hello#world123",
				})
				assert.NoError(t, err, "构造请求体失败")
				// 创建模拟 HTTP 请求
				req, err := http.NewRequest(http.MethodPost,
					"/users/signup", bytes.NewBuffer(reqJSON))
				req.Header.Set("Content-Type", "application/json")
				assert.NoError(t, err)
				return req
			},
			wantCode: http.StatusOK,
			wantBody: "系统异常",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// 初始化 gomock 控制器
			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			// 构造 handler
			userSvc, codeSvc := tc.mock(ctrl)
			hdl := NewUserHandler(userSvc, codeSvc)

			// 搭建 gin 路由（完全模拟真实服务）
			server := gin.Default()
			hdl.RegisterRoutes(server)

			// 创建响应记录器（httptest.ResponseRecorder）：
			//    - 替代真实的 http.ResponseWriter，用于捕获 Gin 处理器的响应
			//    - 可以获取响应状态码、响应体、Header 等信息
			req := tc.reqBuilder(t)
			recorder := httptest.NewRecorder()

			// ===================== 核心步骤5：执行请求并校验结果 =====================
			// 调用 Gin 引擎的 ServeHTTP 方法：
			// - 模拟 HTTP 服务器处理请求的过程：路由匹配 → 执行处理器 → 生成响应
			// - 参数1：recorder（捕获响应），参数2：构造好的请求
			server.ServeHTTP(recorder, req)

			assert.Equal(t, tc.wantCode, recorder.Code)

			// 解析响应体
			var resp map[string]string
			err := json.Unmarshal(recorder.Body.Bytes(), &resp)
			assert.NoError(t, err, "解析响应体失败")
			assert.Equal(t, tc.wantBody, resp["message"], "响应 message 不匹配")
		})
	}
}
