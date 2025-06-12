package main

import "fmt"

func main() {
	//1
	var a = [4]string{"a", "b", "c"}
	for i, v := range a {
		fmt.Println(i, v)
	}
	for i := 0; i < len(a); i++ {
		fmt.Println(a[i])
	}
	//2
	var b = [4]int{2: 4}
	fmt.Println(b)
	//3
	var c = [...]string{"a", "b", "c"}
	fmt.Println(len(c))

	//多维数组
	var d = [3][4]string{
		{"a", "b", "c"},
		{"d", "e", "f"},
	}
	for _, row := range d {
		for _, col := range row {
			fmt.Println("str:", col)
		}
	}
}
