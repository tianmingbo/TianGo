/*
泛型函数
*/
package main

import (
	"cmp"
	"fmt"
)

// Gmap 将 slice 中的每个元素通过 fn 转换，返回新 slice
func Gmap[T any, R any](slice []T, fn func(T) R) []R {
	result := make([]R, len(slice))
	for i, v := range slice {
		result[i] = fn(v)
	}
	return result
}

func Gmin[T cmp.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func index[T comparable](slice []T, b T) int {
	for i, item := range slice {
		if item == b {
			return i
		}
	}
	return -1
}

func main() {
	fmt.Println(index([]int{1, 2, 3}, 3))
	fmt.Println(index([]string{"1", "3", "t"}, "4"))

	fmt.Println(Gmap([]int{1, 2, 3}, func(x int) int { return x * x }))
}
