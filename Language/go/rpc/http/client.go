package main

import (
	"encoding/json"
	"fmt"
	"github.com/kirinlabs/HttpRequest"
)

type AddRes struct {
	Result int `json:"result"`
}

func add(a, b int) int {
	req := HttpRequest.NewRequest()
	res, _ := req.Get(fmt.Sprintf("http://127.0.0.1:8080/add?a=%d&b=%d", a, b))
	body, _ := res.Body()
	fmt.Println(string(body))
	rspData := AddRes{}
	_ = json.Unmarshal(body, &rspData)
	return rspData.Result
}

func main() {
	fmt.Println(add(1, 2))
}
