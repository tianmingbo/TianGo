package main

import "fmt"

type Shape interface {
	setWidth(int)
	Area() int
}

type Rectangle struct {
	width, height int
}

func (r *Rectangle) setWidth(width int) {
	r.width = width
}

func (r Rectangle) Area() int {
	return r.width * r.height
}

func main() {
	//r := Rectangle{5, 5}
	var r Shape = &Rectangle{5, 5}
	r.setWidth(50)
	fmt.Println(r.Area())
}
