package main

import (
	"fmt"
	"time"
)

func main() {
	for i := 0; i < 5; i++ {
		go func() {
			fmt.Println(i) // 可能全部输出 5，因为闭包捕获的是变量引用
		}()
	}
	// 修正：通过参数传递
	for i := 0; i < 5; i++ {
		go func(x int) {
			fmt.Println(x)
		}(i)
	}
	time.Sleep(time.Second)
}
