package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/satori/go.uuid"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	"google.golang.org/grpc/health/grpc_health_v1"

	"lGo/shop/goods_grpc/global"
	"lGo/shop/goods_grpc/handle"
	"lGo/shop/goods_grpc/initialize"
	"lGo/shop/goods_grpc/middleware"
	"lGo/shop/goods_grpc/proto"
	"lGo/shop/goods_grpc/utils"
)

func main() {
	IP := flag.String("ip", "0.0.0.0", "ip地址")
	Port := flag.Int("port", 23333, "端口号")

	zap.S().Info("config:%v", global.Config)
	initialize.InitLogger()
	initialize.InitConfig()
	initialize.InitDB()

	flag.Parse()
	if *Port == 0 {
		*Port, _ = utils.GetFreePort()
	}
	zap.S().Infof("ip: %s port: %d", *IP, *Port)

	listen, err := net.Listen("tcp", fmt.Sprintf("%s:%d", *IP, *Port)) //监听端口
	if err != nil {
		fmt.Println("failed to listen:", err)
	}

	server := grpc.NewServer()                               //创建grpc服务
	proto.RegisterGoodsServer(server, &handle.GoodsServer{}) //注册服务

	//注册服务健康检查
	grpc_health_v1.RegisterHealthServer(server, health.NewServer())

	go func() {
		if err := server.Serve(listen); err != nil {
			panic("failed to start serve!")
		}
	}()

	//服务注册
	addr := fmt.Sprintf("%s:%d", global.Config.ConsulInfo.Host, global.Config.ConsulInfo.Port)
	registerClient, _ := middleware.NewConsulService(addr)
	serviceId := fmt.Sprintf("%s", uuid.NewV4())
	err = registerClient.RegisterService(serviceId, global.Config.Name, global.Config.Host, *Port, global.Config.Tags)
	if err != nil {
		zap.S().Panic("服务注册失败:", err.Error())
	}
	zap.S().Debugf("启动服务器, 端口： %d", *Port)

	//接收终止信号
	quit := make(chan os.Signal)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	if err = registerClient.DeregisterService(serviceId); err != nil {
		zap.S().Info("注销失败:", err.Error())
	} else {
		zap.S().Info("注销成功:")
	}
}
