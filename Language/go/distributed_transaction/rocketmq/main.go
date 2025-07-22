package main

import (
	"context"
	"fmt"
	"time"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/consumer"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

func main() {
	// 初始化RocketMQ生产者（订单服务使用）
	p, err := rocketmq.NewTransactionProducer(
		NewOrderTransactionListener(),
		producer.WithNameServer([]string{"10.6.64.191:9876"}),
		producer.WithGroupName("order_producer_group"),
	)
	if err != nil {
		fmt.Printf("创建生产者失败: %v\n", err)
		return
	}
	if err := p.Start(); err != nil {
		fmt.Printf("启动生产者失败: %v\n", err)
		return
	}
	defer p.Shutdown()

	// 初始化RocketMQ消费者（库存服务使用）
	c, err := rocketmq.NewPushConsumer(
		consumer.WithNameServer([]string{"10.6.64.191:9876"}),
		consumer.WithGroupName("inventory_consumer_group"),
	)
	if err != nil {
		fmt.Printf("创建消费者失败: %v\n", err)
		return
	}

	// 注册库存消息处理器
	inventoryHandler := NewInventoryMessageHandler()
	err = c.Subscribe("order_topic", consumer.MessageSelector{}, inventoryHandler.HandleMessage)
	if err != nil {
		fmt.Printf("订阅主题失败: %v\n", err)
		return
	}

	// 启动消费者
	if err := c.Start(); err != nil {
		fmt.Printf("启动消费者失败: %v\n", err)
		return
	}
	defer c.Shutdown()

	// 初始化测试数据
	inventoryHandler.InitInventory("product_001", 100)

	// 测试正常流程
	fmt.Println("=== 测试正常订单流程 ===")
	orderID := "order_" + time.Now().Format("20060102150405")
	err = CreateOrder(p, orderID, "user_001", "product_001", 10, 999.99)
	if err != nil {
		fmt.Printf("创建订单失败: %v\n", err)
	} else {
		fmt.Printf("订单 %s 创建请求已提交\n", orderID)
	}

	// 等待消息处理
	time.Sleep(5 * time.Second)
	inventory, _ := inventoryHandler.GetInventory("product_001")
	fmt.Printf("产品 %s 当前库存: %d\n", "product_001", inventory.Quantity)

	// 测试库存不足的异常流程
	fmt.Println("\n=== 测试库存不足流程 ===")
	orderID = "order_" + time.Now().Format("20060102150405")
	err = CreateOrder(p, orderID, "user_001", "product_001", 200, 19999.99)
	if err != nil {
		fmt.Printf("创建订单失败: %v\n", err)
	} else {
		fmt.Printf("订单 %s 创建请求已提交\n", orderID)
	}

	// 等待消息处理和回查
	time.Sleep(10 * time.Second)
	inventory, _ = inventoryHandler.GetInventory("product_001")
	fmt.Printf("产品 %s 当前库存: %d\n", "product_001", inventory.Quantity)

	fmt.Println("\n程序执行完成")
}

// 创建订单并发送事务消息
func CreateOrder(producer rocketmq.TransactionProducer, orderID, userID, productID string, quantity int, amount float64) error {
	// 构建订单消息
	msg := BuildOrderMessage(orderID, userID, productID, quantity, amount)

	// 发送半消息
	_, err := producer.SendMessageInTransaction(context.Background(), msg)

	return err
}
