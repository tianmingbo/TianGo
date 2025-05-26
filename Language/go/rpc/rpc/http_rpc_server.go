package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"net/rpc"
)

func main() {
	if err := rpc.RegisterName("Calculator", new(Calculator)); err != nil {
		log.Fatalln(err)
	}
	rpc.HandleHTTP() //注册http处理器
	listen, err := net.Listen("tcp", ":1234")
	if err != nil {
		fmt.Println("Listen error:", err)
		return
	}
	fmt.Println("RPC HTTP 服务运行在 :1234")
	err = http.Serve(listen, nil)
	if err != nil {
		fmt.Println("start err:", err)
		return
	}
}
