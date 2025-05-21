package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	type person struct {
		Name string `json:"name2"` //name2是输出后的key
		Age  int    `json:"age"`
	}
	p := person{Name: "Tian", Age: 18}
	data, err := json.Marshal(p)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(string(data))
	}
}
