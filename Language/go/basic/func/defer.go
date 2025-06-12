package main

import (
	"sync"
	"time"
)

// 多个defer是栈形式执行
// 可以理解为finally. 连接数据库，打开文件，加锁。后使用
func main() {
	mu := sync.Mutex{}
	mu.Lock()
	time.Sleep(time.Second * 2)
	defer mu.Unlock() //放在return之前执行
}
