package main

import (
	"fmt"
	"time"
)

func main() {
	cur := time.Now()
	fmt.Println(cur.Year())
	fmt.Println(cur.Month())
	fmt.Println(cur.Minute())
	fmt.Println(cur.Second())
	fmt.Println(cur.Format(time.DateTime))

	timeStr := "1998-02-09"
	t, _ := time.Parse(time.DateTime, timeStr)
	fmt.Println(cur.Sub(t).Hours())

	timestamp := cur.Unix()
	fmt.Println(timestamp)
	fmt.Println(time.Unix(timestamp, 0))
}
