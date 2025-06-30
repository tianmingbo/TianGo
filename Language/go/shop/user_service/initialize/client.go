package initialize

import (
	"fmt"
	_ "github.com/mbobakov/grpc-consul-resolver"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "lGo/shop/proto"

	"lGo/shop/user_service/global"
)

func InitGrpcClient() {
	conn, err := grpc.NewClient(
		fmt.Sprintf(`consul://%s:%d/user-service?wait=14s`, global.Config.ConsulInfo.Host, global.Config.ConsulInfo.Port),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
	)
	if err != nil {
		zap.S().Fatalf("did not connect: %v", err)
	}
	global.UserClient = pb.NewUserClient(conn) //  创建客户端
	zap.S().Info("init grpc client success")
}
