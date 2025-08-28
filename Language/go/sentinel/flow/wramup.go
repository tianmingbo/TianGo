package main

import (
	"fmt"
	sentinel "github.com/alibaba/sentinel-golang/api"
	"github.com/alibaba/sentinel-golang/core/flow"
	"log"
	"sync"
	"time"
)

var pass sync.Mutex
var failed sync.Mutex
var passCount = 0
var failedCount = 0

func main() {
	err := sentinel.InitDefault()
	if err != nil {
		log.Fatal(err)
	}

	// 配置一条限流规则
	_, err = flow.LoadRules([]*flow.Rule{
		{
			Resource:               "some-test",
			Threshold:              100,
			TokenCalculateStrategy: flow.WarmUp, //预热
			ControlBehavior:        flow.Reject,
			WarmUpPeriodSec:        10,
		},
	})
	if err != nil {
		fmt.Println(err)
		return
	}

	ch := make(chan struct{})
	for i := 0; i < 100; i++ {
		go func() {
			for {
				e, b := sentinel.Entry("some-test")
				if b != nil {
					failed.Lock()
					failedCount += 1
					failed.Unlock()
					//fmt.Println(util.CurrentTimeMillis(), "Rejected", b)
					time.Sleep(time.Second)
				} else {
					pass.Lock()
					passCount += 1
					pass.Unlock()
					//fmt.Println(util.CurrentTimeMillis(), "Passed")
					time.Sleep(time.Second)
					e.Exit()
				}

			}
		}()
	}
	go func() {
		for {
			fmt.Println("pass:", passCount, "failed:", failedCount)
			time.Sleep(time.Second)
		}
	}()
	<-ch
}
