package utils

import (
	"net"
)

// GetFreePort 获取一个空闲端口
func GetFreePort() (int, error) {
	// 绑定 UDP 端口 0，表示让系统分配一个空闲端口
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		return 0, err
	}

	l, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return 0, err
	}

	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port, nil
}
