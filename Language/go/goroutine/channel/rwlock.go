package main

import (
	"fmt"
	"sync"
	"time"
)

type SafeMap struct {
	mu   sync.RWMutex
	data map[string]string
}

func mapInit() *SafeMap {
	return &SafeMap{data: make(map[string]string)}
}

func (smap *SafeMap) Set(key, value string, wg *sync.WaitGroup) {
	smap.mu.Lock()
	defer smap.mu.Unlock()
	defer wg.Done()
	fmt.Println("writing key:", key)
	time.Sleep(time.Second)
	smap.data[key] = value
}

func (smap *SafeMap) Get(key string, wg *sync.WaitGroup) string {
	smap.mu.RLock()
	defer smap.mu.RUnlock()
	defer wg.Done()
	fmt.Println("reading key:", key)
	time.Sleep(500 * time.Millisecond)
	return smap.data[key]
}

func main() {
	smap := mapInit()
	var wg sync.WaitGroup
	wg.Add(4)
	go smap.Set("test", "value1", &wg)

	for i := 0; i < 3; i++ {
		go func(x int) {
			val := smap.Get("test", &wg)
			fmt.Printf("reader %d value: %s\n", x, val)
		}(i)
	}
	wg.Wait()
	fmt.Println("end...")
}
