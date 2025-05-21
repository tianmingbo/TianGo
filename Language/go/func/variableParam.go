package main

import "fmt"

// 不定长参数
func add(items ...int) (sum int, err error) {
	for _, val := range items {
		sum += val
	}
	return
}

func main() {
	a, _ := add(1, 2, 3, 4)
	fmt.Println(a)
}
