package main

import (
	"bytes"
	"context"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"

	"github.com/golang/protobuf/proto"
	"lGo/gin/pb"
)

func main() {

	request := &api.User{
		Name:  "John Doe",
		Age:   30,
		Email: "john@example.com",
	}

	// 将请求序列化为二进制格式
	data, err := proto.Marshal(request)
	if err != nil {
		fmt.Printf("序列化请求失败: %v\n", err)
		os.Exit(1)
	}

	// 创建HTTP请求
	req, err := http.NewRequestWithContext(
		context.Background(),
		"POST",
		"http://localhost:8080/api/users", // 替换为实际API地址
		bytes.NewBuffer(data),
	)
	if err != nil {
		fmt.Printf("创建HTTP请求失败: %v\n", err)
		os.Exit(1)
	}

	// 设置请求头
	req.Header.Set("Content-Type", "application/octet-stream")
	req.Header.Set("Accept", "application/octet-stream")

	// 发送HTTP请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("发送HTTP请求失败: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	// 读取响应数据
	respData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("读取响应失败: %v\n", err)
		os.Exit(1)
	}

	// 解析响应数据
	response := &api.User{}
	if err := proto.Unmarshal(respData, response); err != nil {
		fmt.Printf("解析响应失败: %v\n", err)
		os.Exit(1)
	}

	// 处理响应
	fmt.Printf("请求结果: %v\n", response)
}
