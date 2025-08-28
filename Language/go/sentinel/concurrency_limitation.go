//并发隔离控制

package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	sentinel "github.com/alibaba/sentinel-golang/api"
	"github.com/alibaba/sentinel-golang/core/isolation"
)

func main() {
	err := sentinel.InitDefault()
	if err != nil {
		log.Fatal(err)
	}
	ch := make(chan struct{})

	r1 := &isolation.Rule{
		Resource:   "abc",
		MetricType: isolation.Concurrency, //并发数
		Threshold:  12,
	}
	_, err = isolation.LoadRules([]*isolation.Rule{r1})
	if err != nil {
		fmt.Println(err, "fail")
		os.Exit(1)
	}

	for i := 0; i < 15; i++ {
		go func() {
			e, b := sentinel.Entry("abc", sentinel.WithBatchCount(1))
			if b != nil {
				fmt.Println("[Isolation] Blocked", i, "reason", b.BlockType().String(), "rule", b.TriggeredRule(), "snapshot", b.TriggeredValue())
				time.Sleep(time.Duration(rand.Uint64()%20) * time.Millisecond)
			} else {
				fmt.Println("[Isolation] Passed", i)
				time.Sleep(time.Duration(rand.Uint64()%20) * time.Millisecond)
				e.Exit()
			}
		}()
	}
	<-ch
}
