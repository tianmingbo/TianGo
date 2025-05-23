package main

import (
	"log"
	"net"
	"net/http"
	"net/rpc"
	"time"
)

type Calculator struct{}

type Args struct {
	A int
	B int
}
type Reply struct {
	Result string
}

/*
*
方法必须是公开的（首字母大写）
方法只能有两个参数，一个是传入参数，另一个是返回结果的指针。
func (t *T) MethodName(argType T1, replyType *T2) error
*/
func (c Calculator) Add(arg string, reply *Reply) error {
	time.Sleep(200 * time.Millisecond)
	//reply.Result = arg.A + arg.B
	reply.Result = arg + "hello"
	return nil
}

func main() {
	if err := rpc.RegisterName("Calculator", new(Calculator)); err != nil {
		log.Fatalln(err)
	}
	rpc.HandleHTTP() //注册http处理器
	listen, err := net.Listen("tcp", ":1234")
	if err != nil {
		return
	}
	if err := http.Serve(listen, nil); err != nil {
		log.Fatalln(err)
	}
}
