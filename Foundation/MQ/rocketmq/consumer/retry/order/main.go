/*
* 使用有序消费模型，当 Subscribe 函数返回 consumer.SuspendCurrentQueueAMoment 时，
* 如果 msg.ReconsumeTimes < MaxReconsumeTimes，则会将消息重新发送到本地消息队列以供后续消费；
* 否则，将消息发送到 rocketmq DLQ 主题，我们需要手动解析该消息。
 */
package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/consumer"
	"github.com/apache/rocketmq-client-go/v2/primitive"
)

func main() {
	c, _ := rocketmq.NewPushConsumer(
		consumer.WithGroupName("testRetry"),
		consumer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		consumer.WithConsumerModel(consumer.Clustering),
		consumer.WithConsumeFromWhere(consumer.ConsumeFromFirstOffset), //从最早的消息开始消费
		consumer.WithConsumerOrder(true),                               //启用顺序消费模式
		consumer.WithMaxReconsumeTimes(5),                              //最大重试次数,超过后进入死信队列
	)

	err := c.Subscribe("test", consumer.MessageSelector{},
		func(ctx context.Context, msgs ...*primitive.MessageExt) (consumer.ConsumeResult, error) {
			orderlyCtx, _ := primitive.GetOrderlyCtx(ctx)
			fmt.Printf("orderly context: %v\n", orderlyCtx)
			fmt.Printf("subscribe orderly callback len: %d \n", len(msgs))

			for _, msg := range msgs {
				fmt.Println("重试次数：", msg.ReconsumeTimes)
				if msg.ReconsumeTimes > 5 {
					fmt.Printf("msg ReconsumeTimes > 5. msg: %v", msg)
				} else {
					fmt.Printf("subscribe orderly callback: %v \n", msg)
				}
			}
			//SuspendCurrentQueueAMoment表示消息失败,触发重试
			return consumer.SuspendCurrentQueueAMoment, nil

		})
	if err != nil {
		fmt.Println(err.Error())
	}
	// Note: start after subscribe
	err = c.Start()
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(-1)
	}
	time.Sleep(time.Hour)
	err = c.Shutdown()
	if err != nil {
		fmt.Printf("shundown Consumer error: %s", err.Error())
	}
}
