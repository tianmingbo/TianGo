package main

import (
	"context"
	"fmt"
	"github.com/apache/rocketmq-client-go/v2/consumer"
	"log"
	"time"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

func main() {
	// 创建生产者
	p, err := rocketmq.NewProducer(
		producer.WithGroupName("testGroup"),
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{"127.0.0.1:9876"})),
	)
	if err != nil {
		log.Fatalf("创建生产者失败: %s", err.Error())
	}

	// 启动生产者
	err = p.Start()
	if err != nil {
		log.Fatalf("启动生产者失败: %s", err.Error())
	}

	// 指定队列 ID 发送消息
	sendMessageToSpecificQueue(p, "testTopic", 2) // 指定发送到队列 ID 为 2 的队列

	// 关闭生产者
	err = p.Shutdown()
	if err != nil {
		log.Fatalf("关闭生产者失败: %s", err.Error())
	}

}

// sendMessageToSpecificQueue 发送消息到指定的队列
func sendMessageToSpecificQueue(p rocketmq.Producer, topic string, queueID int) {
	// 创建消息
	msg := &primitive.Message{
		Topic: topic,
		Body:  []byte("Hello RocketMQ! 指定队列 ID 示例"),
	}

	// 获取主题的队列元数据
	queues, err := p.GetTopicRouteInfoManager().GetTopicQueues(topic)
	if err != nil {
		log.Fatalf("获取主题队列信息失败: %s", err.Error())
	}

	// 确保指定的队列 ID 存在
	if queueID >= len(queues) {
		log.Fatalf("指定的队列 ID %d 不存在，该主题共有 %d 个队列", queueID, len(queues))
	}

	// 发送消息到指定队列
	result, err := p.SendSync(context.Background(), msg,
		// 自定义队列选择器，始终选择指定的队列
		producer.WithQueueSelector(producer.NewManualQueueSelector(queues[queueID])))

	if err != nil {
		log.Fatalf("发送消息到指定队列失败: %s", err.Error())
	}

	fmt.Printf("消息发送成功: 队列ID=%d, 消息ID=%s\n", queueID, result.MsgID)
}
