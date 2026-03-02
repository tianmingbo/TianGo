package main

import "fmt"

type stack[T any] struct {
	items []T
}

func (s *stack[T]) push(item T) {
	s.items = append(s.items, item)
}
func (s *stack[T]) pop() (T, bool) {
	if len(s.items) == 0 {
		var zero T
		return zero, false
	}
	item := s.items[0]
	s.items = s.items[1:]
	return item, true
}

func main() {
	intStack := &stack[int]{}
	v, ok := intStack.pop()
	fmt.Println(v, ok)
	intStack.push(3)
	v, ok = intStack.pop()
	fmt.Println(v, ok)

	stringStack := &stack[string]{}
	stringStack.push("hello")
	stringStack.push("world")
	if v, ok := stringStack.pop(); ok {
		fmt.Println(v)
	}
}
