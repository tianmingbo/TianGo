package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"net/rpc/jsonrpc"
)

func main() {
	a := flag.Int("a", 0, "第一个数字")
	b := flag.Int("b", 0, "第二个数字")
	flag.Parse()
	fmt.Println(*a, *b)

	conn, err := net.Dial("tcp", "localhost:1234")
	if err != nil {
		fmt.Println("连接失败:", err)
		return
	}
	client := jsonrpc.NewClient(conn)

	defer client.Close()
	var reply Reply
	args := Args{
		A: *a,
		B: *b,
	}
	err = client.Call("Calculator.Add", args, &reply)
	if err != nil {
		log.Fatalln("call", err)
		return
	}
	fmt.Println("res: ", reply.Result)
}
