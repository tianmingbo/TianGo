package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

func addItem(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Println(r.URL.Path)
	_ = r.ParseForm()
	a, _ := strconv.Atoi(r.Form["a"][0])
	b, _ := strconv.Atoi(r.Form["b"][0])
	jData, _ := json.Marshal(map[string]int{"result": a + b})
	_, _ = w.Write(jData)
}

func main() {
	// 注册路由
	http.HandleFunc("/add", addItem)

	// 启动服务器
	fmt.Println("Server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
