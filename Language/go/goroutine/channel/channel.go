package main

import (
	"fmt"
	"time"
)

var ch1 = make(chan bool)
var ch2 = make(chan bool)

func printNum() {
	i := 0
	for {
		<-ch1
		fmt.Printf(" %d %d", i, i+1)
		i += 2
		ch2 <- true
	}

}

func printLetter() {
	i := 0
	for {
		str := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		if i > len(str)-1 {
			i = 0
		}
		<-ch2
		fmt.Print(str[i : i+2])
		i += 2
		ch1 <- true
	}

}

func main() {
	go printNum()
	go printLetter()
	ch1 <- true
	time.Sleep(time.Second * 1)
}
