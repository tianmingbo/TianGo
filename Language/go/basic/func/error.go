package main

import (
	"errors"
	"fmt"
)

func test(a int) (int, error) {
	return 0, errors.New("test error")
}

func testPanic() {
	//recover捕获错误，只有在defer调用的函数中才会生效
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("occur a error:", r)
		}
	}()
	var b map[int]int
	b[0] = 0
}

func main() {
	if res, err := test(5); err != nil {
		fmt.Println(res, err.Error())
	}

	//panic 退出程序
	testPanic()
}
