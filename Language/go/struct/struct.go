package main

import "fmt"

type Student struct {
	name string
	age  int
	//p    Person
	Person //匿名嵌套
}
type Person struct {
	name   string
	age    int
	addr   string
	height float32
}

// 绑定方法，格式：
// func (s StructType) funcName(param1)(return val){}
func (s Student) getName() string {
	return s.name
}

func main() {
	p1 := Person{height: 5.5}
	p2 := Person{"tian", 18, "SH", 1.8}
	var p3 Person
	p3.age = 19
	pL := []Person{p1, {
		name: "tian",
	}}
	pL = append(pL, p2, p3)
	fmt.Println(pL)
	//匿名结构体
	address := struct {
		city     string
		province string
	}{"<HN>", "<ZZ>"}
	fmt.Println(address.city, address.province)
	//结构体嵌套
	var s Student
	s.name = "tian"
	s.Person.name = "tian2" //给匿名结构体赋值
	s.age = 18
	s.addr = "sh"
	fmt.Println(s.getName())
}
