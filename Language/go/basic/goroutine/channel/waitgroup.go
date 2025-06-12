package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

var wg sync.WaitGroup

func test() {
	defer wg.Done()
	time.Sleep(time.Second)
	fmt.Println(rand.Intn(10))
}

func main() {
	wg.Add(100)
	for i := 0; i < 100; i++ {
		go test()
	}
	wg.Wait()
}
