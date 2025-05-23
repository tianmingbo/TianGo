package main

import (
	"encoding/json"
	"fmt"
	"github.com/levigross/grequests"
	"log"
)

type AddRes struct {
	Result int `json:"result"`
}

func add(a, b int) int {
	url := fmt.Sprintf("http://127.0.0.1:8080/add?a=%d&b=%d", a, b)

	resp, err := grequests.Get(url, nil)
	if err != nil {
		log.Fatal(err)
	}
	rspData := AddRes{}
	_ = json.Unmarshal(resp.Bytes(), &rspData)
	return rspData.Result
}

func main() {
	fmt.Println(add(1, 2))
}
