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

// 使用并发消费模型，当 Subscribe 函数返回 consumer.ConsumeRetryLater 时，消息将被发送到 retry topic。
// 可以在 ConsumeConcurrentlyContext 中设置 DelayLevelWhenNextConsume，用于设置消息从retry topic重新发送到原始topic的延迟时间。
//
// 本例中，我们始终设置 DelayLevelWhenNextConsume=1，表示消息将在 1 秒后发送到原始topic。
// 在无限次重试的情况下，在 ReconsumeTimes > 5 后返回 consumer.ConsumeSuccess
func main() {
	c, _ := rocketmq.NewPushConsumer(
		consumer.WithGroupName("testRetry2"),
		consumer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		consumer.WithConsumerModel(consumer.Clustering),
	)

	// DelayLevel指定下次消息被重新消费的时间间隔，范围是1~18
	// 分别对应[1s, 5s, 10s, 30s,1m, 2m, 3m, 4m, 5m, 6m, 7m, 8m, 9m, 10m, 20m, 30m, 1h, 2h]
	delayLevel := 1
	err := c.Subscribe("test", consumer.MessageSelector{},
		func(ctx context.Context, msgs ...*primitive.MessageExt) (consumer.ConsumeResult, error) {
			fmt.Printf("subscribe callback len: %d \n", len(msgs))

			concurrentCtx, _ := primitive.GetConcurrentlyCtx(ctx)
			concurrentCtx.DelayLevelWhenNextConsume = delayLevel // only run when return consumer.ConsumeRetryLater

			for _, msg := range msgs {
				if msg.ReconsumeTimes > 5 {
					fmt.Printf("msg ReconsumeTimes > 5. msg: %v", msg)
					return consumer.ConsumeSuccess, nil
				} else {
					fmt.Printf("subscribe callback: %v \n", msg)
				}
			}
			return consumer.ConsumeRetryLater, nil
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
