package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int, 2)
	go func(ch chan int) {
		for data := range ch {
			fmt.Println(data)
		}
		fmt.Println("close channel")
	}(ch)
	ch <- 1
	ch <- 2
	close(ch) //关闭channel
	d := <-ch //已关闭的channel可以继续读值，不可以继续写值
	fmt.Println(d)
	time.Sleep(time.Second * 5)
}
