package main

import (
	"flag"
	"fmt"
	"log"
	"net/rpc"
)

func main() {
	a := flag.Int("a", 0, "第一个数字")
	b := flag.Int("b", 0, "第二个数字")
	flag.Parse()
	fmt.Println(*a, *b)
	client, err := rpc.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		return
	}
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
