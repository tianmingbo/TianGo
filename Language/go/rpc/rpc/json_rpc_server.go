package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
	"net/rpc/jsonrpc"
)

func main() {
	if err := rpc.RegisterName("Calculator", new(Calculator)); err != nil {
		log.Fatalln(err)
	}
	listener, err := net.Listen("tcp", ":1234")
	if err != nil {
		return
	}
	// 接收连接
	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("连接失败:", err)
			continue
		}
		fmt.Println("connect success: ", conn.RemoteAddr())
		go jsonrpc.ServeConn(conn) // 处理请求
	}
}
