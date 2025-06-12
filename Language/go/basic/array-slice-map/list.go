package main

import (
	"container/list"
	"fmt"
)

func main() {
	//链表实现
	//l := list.List{}
	l := list.New() //同上
	l.PushBack(1)
	l.PushBack(2)
	l.PushBack(3)
	l.PushFront(6)
	for e := l.Front(); e != nil; e = e.Next() {
		if e.Value == 2 {
			l.InsertBefore(7, e)
		}
		fmt.Println(e.Value)
	}
	fmt.Println()
	//反向遍历
	for e := l.Back(); e != nil; e = e.Prev() {
		fmt.Println(e.Value)
	}
}
