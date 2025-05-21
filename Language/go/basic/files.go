package main

import (
	"fmt"
	"os"
)

func main() {

	dir, err := os.ReadDir("./basic")
	if err != nil {
		return
	}
	for _, entry := range dir {
		fmt.Println(entry.Name())
	}

	//文件读取
	data, err := os.ReadFile("./basic/array.go")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(string(data))

	//写文件
	WriteData := []byte("Tian test\n go file")
	err = os.WriteFile("./basic/test.txt", WriteData, 0666)
	if err != nil {
		fmt.Println("write err", err)
	}

	//文件打开
	file, err := os.OpenFile("./basic/test.txt", os.O_RDWR|os.O_CREATE, 0666)
	if err != nil {
		return
	}
	defer file.Close()
}
