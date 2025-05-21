package main

import "fmt"

type Person struct {
	Name string
	Age  int
}

func swap(a, b *int) {
	*a, *b = *b, *a
}

func addAge(p *Person) {
	p.Age++
}

func main() {
	p := &Person{Name: "tian", Age: 10}
	(*p).Name = "tian1"
	p.Name = "tian2" //go做了优化,自动解引用
	addAge(p)
	fmt.Println(p.Name, p.Age)

	a1, b := 1, 2
	swap(&a1, &b)
	fmt.Println(a1, b)

	var a = [3]int{1, 2, 3}
	var pa *[3]int = &a //数组的指针，指向整个数组
	//for _, p := range *pa {
	for _, p := range pa { //同上
		fmt.Println(p)
	}

	var ps [3]*int //指针数组，每个元素都是*int
	for i := 0; i < 3; i++ {
		ps[i] = &i
	}
	fmt.Println(ps)
}
