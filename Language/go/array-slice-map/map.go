package main

import (
	"fmt"
)

func main() {
	//初始化
	var a = map[string]int{} //必须初始化才能使用
	a["go"] = 1
	a["java"] = 1
	a["py"] = 1

	var b = make(map[string]int)
	b["go"] = 1
	fmt.Println(a, b)

	//遍历, map是无序的
	for k, v := range b {
		fmt.Println(k, v)
	}
	for k := range b {
		fmt.Println(k, b[k])
	}

	//查
	if v, ok := a["java"]; ok {
		fmt.Println(v)
	} else {
		fmt.Println("not found")
	}
	//删除
	delete(a, "go")
	fmt.Println(a)

	//map不是线程安全的sync.Map{}
}
