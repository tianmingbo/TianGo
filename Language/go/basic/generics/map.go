package main

import "fmt"

type pair[K comparable, V any] struct {
	Key   K
	Value V
}

// 返回 map 中所有键值对
func pairs[K comparable, V any](m map[K]V) []pair[K, V] {
	pairs := make([]pair[K, V], 0, len(m))
	for k, v := range m {
		pairs = append(pairs, pair[K, V]{k, v})
	}
	return pairs
}

func main() {
	m := make(map[string]int, 10)
	m["py"] = 1
	m["golang"] = 2
	fmt.Println(pairs(m))
}
