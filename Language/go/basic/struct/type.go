package main

import "fmt"

type myInt = int //类型别名，完全等价于 int
type myInt2 int  //定义了一个新类型，底层是 int
/*
type:
1.定义结构体
2.定义接口
3.定义类型别名
4.类型定义
5.类型判断
*/
func main() {
	var i myInt
	fmt.Printf("%T", i)
}
