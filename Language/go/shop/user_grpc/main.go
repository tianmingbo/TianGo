package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"lGo/shop/user_service/proto"
	"log"
	"net"
	"runtime/debug"
	"sync/atomic"
	"time"

	"google.golang.org/grpc"

	"lGo/shop/user_grpc/handle"
)

// 服务状态管理
const (
	StatusRunning int32 = iota
	StatusRecovering
)

type RecoveryInterceptor struct {
	serviceStatus int32
}

func NewRecoveryInterceptor() *RecoveryInterceptor {
	return &RecoveryInterceptor{
		serviceStatus: StatusRunning,
	}
}

// 拦截器实现
func (r *RecoveryInterceptor) UnaryInterceptor() grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		// 检查服务是否正在恢复
		if atomic.LoadInt32(&r.serviceStatus) == StatusRecovering {
			return nil, status.Errorf(codes.Unavailable, "服务暂时不可用，请稍后重试")
		}

		defer func() {
			if p := recover(); p != nil {
				atomic.StoreInt32(&r.serviceStatus, StatusRecovering)

				stack := debug.Stack()
				log.Printf("💥 致命错误: %v\n%s", p, stack)

				go r.recoverService(info.FullMethod)

				// 返回标准化错误
				//panic(status.Errorf(codes.Internal, "服务暂时不可用，请稍后重试"))
			}
		}()

		return handler(ctx, req)
	}
}

// 服务恢复逻辑
func (r *RecoveryInterceptor) recoverService(method string) {
	log.Printf("🚑 开始恢复服务，异常来自: %s", method)

	// 模拟恢复耗时
	time.Sleep(2 * time.Second)

	// 恢复完成
	atomic.StoreInt32(&r.serviceStatus, StatusRunning)
	log.Println("✅ 服务已恢复正常")
}

func main() {
	listen, err := net.Listen("tcp", ":23333") //监听端口
	if err != nil {
		fmt.Println("failed to listen:", err)
	}

	//recoveryInterceptor := NewRecoveryInterceptor()
	s := grpc.NewServer()                             //创建grpc服务
	proto.RegisterUserServer(s, &handle.UserServer{}) //注册服务
	fmt.Println("gRPC server listening on :23333")
	if err := s.Serve(listen); err != nil {
		fmt.Println("failed to serve:", err)
	}
}
