// 实现多个接口
package main

import (
	"fmt"
	"os"
)

type Reader interface {
	Read() (n int, err error)
}
type Writer interface {
	Write(p []byte) (n int, err error)
}

type ReadWriter interface {
	Reader
	Writer
}

type Db struct{}

func (r Db) Read() (n int, err error) {
	file, err := os.ReadFile("./basic/test.txt")
	fmt.Println(string(file))
	return len(file), err
}

func (w Db) Write(p []byte) (n int, err error) {
	return len(p), os.WriteFile("./basic/test.txt", p, 0666)
}

func main() {
	var d ReadWriter = Db{}
	writeData := []byte("hello world")
	if writeLen, err := d.Write(writeData); err != nil {
		fmt.Println("write data len:", writeLen)
	}
	d.Read()
}
