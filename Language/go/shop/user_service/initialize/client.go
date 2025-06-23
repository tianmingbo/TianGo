package initialize

import (
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"lGo/shop/user_service/global"
	pb "lGo/shop/user_service/proto"
	"log"
)

func InitGrpcClient() {
	conn, err := grpc.NewClient("127.0.0.1:23333", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	global.UserClient = pb.NewUserClient(conn) //  创建客户端
	zap.S().Info("init grpc client success")
}
