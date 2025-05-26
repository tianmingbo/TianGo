package main

import (
	"context"
	"fmt"
	"math/rand"
	"time"
)

func worker(ctx context.Context, ch chan int) {
	fmt.Println(ctx.Value("key").(int))
	for {
		select {
		case <-ctx.Done():
			close(ch)
			return //结束
		default:
			ch <- rand.Intn(100)
			time.Sleep(time.Millisecond * 500)
		}
	}
}

func main() {
	ch := make(chan int)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second) //带超时
	ctx = context.WithValue(ctx, "key", 100)                                //带值
	defer cancel()
	go worker(ctx, ch)

	for data := range ch {
		fmt.Println("received:", data)
	}
	fmt.Println("done")
}
