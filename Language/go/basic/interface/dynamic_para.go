// 动态类型传参
package main

import (
	"fmt"
	"strconv"
)

func add(a, b interface{}) (int, error) {
	//fmt.Printf("%T, %v\n", a, a)
	//fmt.Printf("%T, %v\n", b, b)
	//断言
	return a.(int) + b.(int), nil
}

func add1(a, b interface{}) (int, error) {
	switch a.(type) {
	case int:
		return a.(int) + b.(int), nil
	case float64:
		return int(a.(float64) + b.(float64)), nil
	case string:
		aStr, ok1 := a.(string)
		bStr, ok2 := b.(string)
		if ok1 || ok2 {
			return 0, fmt.Errorf("类型断言失败")
		}
		aInt, _ := strconv.Atoi(aStr)
		bInt, _ := strconv.Atoi(bStr)
		return aInt + bInt, nil
	default:
		return 0, fmt.Errorf("不支持的类型")
	}

}

func main() {
	add(1, 2)

	if res, err := add1("1", 2); err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(res)
	}

}
