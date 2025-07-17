/**
 * use orderly consumer model, when Subscribe function return consumer.SuspendCurrentQueueAMoment, it will be re-send to
 * local msg queue for later consume if msg.ReconsumeTimes < MaxReconsumeTimes, otherwise, it will be send to rocketmq
 * DLQ topic, we should manually resolve the msg.
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
		consumer.WithGroupName("testGroup"),
		consumer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		consumer.WithConsumerModel(consumer.Clustering),
		consumer.WithConsumeFromWhere(consumer.ConsumeFromFirstOffset),
		consumer.WithConsumerOrder(true),
		consumer.WithMaxReconsumeTimes(5),
	)

	err := c.Subscribe("TopicTest", consumer.MessageSelector{}, func(ctx context.Context,
		msgs ...*primitive.MessageExt) (consumer.ConsumeResult, error) {
		orderlyCtx, _ := primitive.GetOrderlyCtx(ctx)
		fmt.Printf("orderly context: %v\n", orderlyCtx)
		fmt.Printf("subscribe orderly callback len: %d \n", len(msgs))

		for _, msg := range msgs {
			if msg.ReconsumeTimes > 5 {
				fmt.Printf("msg ReconsumeTimes > 5. msg: %v", msg)
			} else {
				fmt.Printf("subscribe orderly callback: %v \n", msg)
			}
		}
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
