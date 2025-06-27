package middleware

import (
	"fmt"
	"github.com/hashicorp/consul/api"
	"log"
)

// ConsulService 表示注册到Consul的服务
type ConsulService struct {
	Client *api.Client
}

// NewConsulService 创建一个新的Consul服务客户端
func NewConsulService(addr string) (*ConsulService, error) {
	config := api.DefaultConfig()
	config.Address = addr

	client, err := api.NewClient(config)
	if err != nil {
		return nil, fmt.Errorf("创建Consul客户端失败: %v", err)
	}

	return &ConsulService{Client: client}, nil
}

// RegisterService 注册服务到Consul
func (cs *ConsulService) RegisterService(id, name, address string, port int, tags []string) error {
	registration := &api.AgentServiceRegistration{
		ID:      id,
		Name:    name,
		Tags:    tags,
		Address: address,
		Port:    port,
		Check: &api.AgentServiceCheck{
			GRPC:                           fmt.Sprintf("%s:%d", address, port),
			Interval:                       "10s",
			Timeout:                        "3s",
			DeregisterCriticalServiceAfter: "1m",
		},
	}

	return cs.Client.Agent().ServiceRegister(registration)
}

// DeregisterService 从Consul注销服务
func (cs *ConsulService) DeregisterService(serviceID string) error {
	return cs.Client.Agent().ServiceDeregister(serviceID)
}

// UpdateService 更新Consul中的服务
func (cs *ConsulService) UpdateService(id, name, address string, port int, tags []string) error {
	// 先注销原有服务
	if err := cs.DeregisterService(id); err != nil {
		log.Printf("注销旧服务失败: %v", err)
	}

	// 注册新服务
	return cs.RegisterService(id, name, address, port, tags)
}

// GetService 获取Consul中的服务
func (cs *ConsulService) GetService(serviceName string) ([]*api.ServiceEntry, error) {
	health := cs.Client.Health()
	services, _, err := health.Service(serviceName, "", true, nil)
	if err != nil {
		return nil, fmt.Errorf("获取服务失败: %v", err)
	}

	return services, nil
}

func main() {
	// 创建Consul客户端
	//consul, err := NewConsulService("10.6.64.191:8500")
	//if err != nil {
	//	log.Fatalf("初始化Consul客户端失败: %v", err)
	//}

	// 注册服务
	//err = consul.RegisterService(
	//	"user-service-1",
	//	"user-service",
	//	"10.6.64.239",
	//	8888,
	//	[]string{"v1", "TEST"},
	//)
	//if err != nil {
	//	log.Fatalf("注册服务失败: %v", err)
	//}
	//log.Println("服务注册成功")

	// 查询服务
	//services, err := consul.GetService("user-service")
	//if err != nil {
	//	log.Fatalf("查询服务失败: %v", err)
	//}
	//log.Printf("找到 %d 个服务实例", len(services))
	//for _, service := range services {
	//	log.Printf("服务: %s, 地址: %s:%d",
	//		service.Service.ID,
	//		service.Service.Address,
	//		service.Service.Port,
	//	)
	//}
	//
	// 更新服务
	//err = consul.UpdateService(
	//	"user-service-2",
	//	"user-service",
	//	"10.6.64.239",
	//	8888,                     // 更新端口
	//	[]string{"v2", "211111"}, // 更新标签
	//)
	//if err != nil {
	//	log.Fatalf("更新服务失败: %v", err)
	//}
	//log.Println("服务更新成功")

	// 删除服务
	//err = consul.DeregisterService("user-service-1")
	//if err != nil {
	//	log.Fatalf("删除服务失败: %v", err)
	//}
	//log.Println("服务删除成功")
}
