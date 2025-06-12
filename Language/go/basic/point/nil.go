package main

import "fmt"

func main() {
	//struct默认值不是nil
	var p *int           // 指针为 nil
	var m map[string]int // map 为 nil
	var s []int          // slice 为 nil
	var ch chan int      // channel 为 nil
	var f func()         // func 为 nil
	var i interface{}    // interface 为 nil

	fmt.Println(p == nil, m == nil, s == nil, ch == nil, f == nil, i == nil) //true true true true true true
}
