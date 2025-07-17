// Package main implements a producer with user custom interceptor.
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/apache/rocketmq-client-go/v2"
	"github.com/apache/rocketmq-client-go/v2/primitive"
	"github.com/apache/rocketmq-client-go/v2/producer"
)

func main() {
	p, _ := rocketmq.NewProducer(
		producer.WithNsResolver(primitive.NewPassthroughResolver([]string{"10.6.64.191:9876"})),
		producer.WithRetry(2),
		producer.WithInterceptor(UserFirstInterceptor(), UserSecondInterceptor()),
	)
	err := p.Start()
	if err != nil {
		fmt.Printf("start producer error: %s", err.Error())
		os.Exit(1)
	}
	for i := 0; i < 10; i++ {
		res, err := p.SendSync(context.Background(), primitive.NewMessage("test",
			[]byte("Hello RocketMQ Go Client!")))

		if err != nil {
			fmt.Printf("send message error: %s\n", err)
		} else {
			fmt.Printf("send message success: result=%s\n", res.String())
		}
	}
	err = p.Shutdown()
	if err != nil {
		fmt.Printf("shutdown producer error: %s", err.Error())
	}
}

func UserFirstInterceptor() primitive.Interceptor {
	return func(ctx context.Context, req, reply interface{}, next primitive.Invoker) error {
		fmt.Printf("user first interceptor before invoke: req:%v\n", req)
		err := next(ctx, req, reply)
		fmt.Printf("user first interceptor after invoke: req: %v, reply: %v \n", req, reply)
		return err
	}
}

func UserSecondInterceptor() primitive.Interceptor {
	return func(ctx context.Context, req, reply interface{}, next primitive.Invoker) error {
		fmt.Printf("user second interceptor before invoke: req: %v\n", req)
		err := next(ctx, req, reply)
		fmt.Printf("user second interceptor after invoke: req: %v, reply: %v \n", req, reply)
		return err
	}
}
