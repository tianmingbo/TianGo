package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)
	go func() {
		time.Sleep(time.Second)
		ch1 <- "from one"
	}()

	go func() {
		time.Sleep(time.Second * 2)
		ch2 <- "from two"
	}()

	select {
	case data := <-ch1:
		fmt.Println(data)
	case data2 := <-ch2:
		fmt.Println(data2)
	}
}
