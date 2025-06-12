package main

import (
	"fmt"
	"time"
)

func consumer(ch <-chan int) {
	//read only
	for num := range ch {
		fmt.Println(num)
	}
}
func producer(ch chan<- int) {
	//write only
	for i := 0; i < 10; i++ {
		ch <- i
	}
	close(ch)
}

func main() {
	ch := make(chan int)
	go producer(ch)
	go consumer(ch)
	time.Sleep(1 * time.Second)
}
