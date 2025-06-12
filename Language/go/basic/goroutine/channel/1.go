package main

import (
	"fmt"
	"time"
)

func getMsg(ch chan int) {
	data := <-ch
	fmt.Println(data)
}

func main() {
	ch := make(chan int)
	ch <- 10
	go getMsg(ch)
	time.Sleep(time.Second)
}
