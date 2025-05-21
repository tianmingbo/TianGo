package main

import "fmt"

func main() {
	var a = "test"
	switch a {
	case "tes":
		fmt.Println("tes")
	case "t", "test": //使用逗号分隔
		fmt.Println("666")
		fallthrough //执行下一个分支，默认不会往下执行，不像C需要显式break
	case "e":
		fmt.Println("e")
	default:
		fmt.Println("unknown")
	}
}
