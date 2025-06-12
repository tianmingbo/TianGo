package main

import (
	"fmt"
)

// 返回一个“带缓存”的 Fibonacci 函数（闭包）
func fibonacciWithCache() func(int) int {
	cache := make(map[int]int) // 闭包“记住”的状态（外部变量）

	var fib func(n int) int
	fib = func(n int) int {
		if n <= 1 {
			return n
		}
		// 查缓存
		if val, ok := cache[n]; ok {
			return val
		}
		// 递归 + 存缓存
		cache[n] = fib(n-1) + fib(n-2)
		return cache[n]
	}

	return fib // 返回闭包
}

func main() {
	fib := fibonacciWithCache()

	// 计算 fib(10)
	for i := 0; i <= 10; i++ {
		fmt.Printf("fib(%d) = %d\n", i, fib(i))
	}
}
