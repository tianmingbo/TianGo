package main

import (
	"bytes"
	"context"
	"fmt"
	"time"

	"github.com/spf13/viper"
	"go.etcd.io/etcd/client/v3"
)

// 初始化etcd客户端
func newEtcdClient() (*clientv3.Client, error) {
	config := clientv3.Config{
		Endpoints:   []string{"10.6.64.191:2379"},
		DialTimeout: 5 * time.Second,
	}
	client, err := clientv3.New(config)
	if err != nil {
		return nil, fmt.Errorf("创建etcd客户端失败: %v", err)
	}
	return client, nil
}

// Viper加载etcd配置（兼容低版本：替换ReadConfigBytes）
func viperLoadFromEtcd(client *clientv3.Client, key string) (*viper.Viper, error) {
	// 1. 从etcd读取配置
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	resp, err := client.Get(ctx, key)
	cancel()
	if err != nil {
		return nil, fmt.Errorf("读取etcd配置失败: %v", err)
	}
	if len(resp.Kvs) == 0 {
		return nil, fmt.Errorf("etcd中不存在key: %s", key)
	}

	// 2. 低版本Viper加载配置
	v := viper.New()
	v.SetConfigType("yaml")
	// 用bytes.Buffer封装字节数组，适配ReadConfig(io.Reader)
	configBuffer := bytes.NewBuffer(resp.Kvs[0].Value)
	err = v.ReadConfig(configBuffer)
	if err != nil {
		return nil, fmt.Errorf("Viper加载配置失败: %v", err)
	}
	return v, nil
}

// 监听etcd配置变更（兼容低版本：替换ReadConfigBytes和Reset）
func watchEtcdConfig(client *clientv3.Client, key string, v *viper.Viper) {
	watchChan := client.Watch(context.Background(), key)
	fmt.Println("开始监听etcd配置变更...")

	for watchResp := range watchChan {
		for _, event := range watchResp.Events {
			fmt.Printf("配置变更: 类型=%s, key=%s, 新值=%s\n", event.Type, event.Kv.Key, event.Kv.Value)
			if event.Type == clientv3.EventTypePut {
				v.SetConfigType("yaml")
				buf := bytes.NewBuffer(event.Kv.Value)
				err := v.ReadConfig(buf)
				if err != nil {
					fmt.Printf("更新Viper配置失败: %v\n", err)
					continue
				}

				var cfg Config
				err = v.Unmarshal(&cfg)
				if err != nil {
					return
				}
				// 验证更新结果
				fmt.Println("更新后配置：", cfg)
			} else if event.Type == clientv3.EventTypeDelete {
				fmt.Println("配置被删除！")
			}
		}
	}
}

func main() {
	// 1. 创建etcd客户端
	client, err := newEtcdClient()
	if err != nil {
		fmt.Printf("客户端初始化失败: %v\n", err)
		return
	}
	defer client.Close()

	// 2. 写入测试配置（确保etcd中有数据，方便测试）
	testConfig := `
name: "my-go-app"
server:
  port: 8080
  debug: true
  allowed_ips:
    - "127.0.0.1"
    - "192.168.1.0/24"
mysql:
  host: "127.0.0.1"
  port: 3306
  user: "root"
  password: "123456"
redis:
  host: "127.0.0.1"
  port: 6379
  password: ""
  db: 0
`
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	_, err = client.Put(ctx, "/config/app", testConfig)
	cancel()
	if err != nil {
		fmt.Printf("写入测试配置失败: %v\n", err)
		return
	}

	// 3. Viper加载etcd配置
	configKey := "/config/app"
	v, err := viperLoadFromEtcd(client, configKey)
	if err != nil {
		fmt.Printf("Viper加载etcd配置失败: %v\n", err)
		return
	}

	var cfg Config
	err = v.Unmarshal(&cfg)
	if err != nil {
		return
	}
	fmt.Println("config:", cfg)

	// 5. 后台监听配置变更
	go watchEtcdConfig(client, configKey, v)

	// 保持程序运行（按Ctrl+C退出）
	fmt.Println("程序已启动，可修改/删除etcd配置测试热更新...")
	select {}
}
