package main

import "fmt"

func removeAt(s []string, index int) []string {
	return append(s[:index], s[index+1:]...)
}

func main() {
	//slice初始化

	//从数组创建
	//a := [4]int{1, 2, 3}
	//b := a[:3]

	//直接创建
	//b := []int{1, 2, 3}
	//fmt.Println(b)

	//make
	b := make([]int, 3) //长度 3，初始为 [0 0 0]
	b = append(b, 1, 2)
	for _, v := range b {
		fmt.Println(v)
	}

	s1 := []string{"a", "b"}
	s2 := []string{"c", "d", "e"}
	s1 = append(s1, s2[1:]...)
	fmt.Println(s1)

	//删除元素
	s2 = removeAt(s2, 1)
	fmt.Println(s2)

	//copy 深拷贝
	s3 := make([]string, len(s2))
	copy(s3, s2)
	fmt.Println("s3:", s3)
}
