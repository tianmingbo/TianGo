package main

import (
	"fmt"
	"sync"
)

var lock sync.Mutex

var num = 0

func add(wg *sync.WaitGroup) {
	defer wg.Done()
	lock.Lock()
	defer lock.Unlock()
	num++
}

func sub(wg *sync.WaitGroup) {
	defer wg.Done()
	lock.Lock()
	defer lock.Unlock()
	num--
}

func main() {
	var wg sync.WaitGroup
	wg.Add(200000)
	for i := 0; i < 100000; i++ {
		go add(&wg)
	}
	for i := 0; i < 100000; i++ {
		go sub(&wg)
	}
	wg.Wait()
	fmt.Println("final num is: ", num)
}
