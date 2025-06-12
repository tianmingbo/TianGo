package main

import "fmt"

func testSlice(s []string) {
	//看似是把值传递过来了，但是实际上只是复制了slice。slice其实也只是指向了原来的数组
	fmt.Println(s)
	s[0] = "d"
}

func main() {
	a := []string{"a", "b", "c", "d", "e", "f", "g"}
	testSlice(a)
	fmt.Println(a)
	s1 := a[1:5]
	s2 := a[3:5]
	//▄█▀█●
	s2[0] = "ttt"
	fmt.Println(cap(s1), "s1:", s1) //6 s1: [b c ttt e]
	fmt.Println(cap(s2), "s2:", s2) //4 s2: [ttt e]
}
