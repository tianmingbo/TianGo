package main

import (
	"fmt"
	sentinel "github.com/alibaba/sentinel-golang/api"
	"github.com/alibaba/sentinel-golang/core/flow"
	"github.com/alibaba/sentinel-golang/util"
	"log"
	"time"
)

func main() {
	// 务必先进行初始化
	err := sentinel.InitDefault()
	if err != nil {
		log.Fatal(err)
	}

	// 配置一条限流规则
	_, err = flow.LoadRules([]*flow.Rule{
		{
			Resource:               "some-test", //资源名
			Threshold:              10,
			TokenCalculateStrategy: flow.Direct, //当前流量控制器的Token计算策略。Direct表示直接使用字段 Threshold 作为阈值；WarmUp表示使用预热方式计算Token的阈值。
			ControlBehavior:        flow.Reject, //流量控制器的控制策略；Reject表示超过阈值直接拒绝，Throttling表示匀速排队。
			StatIntervalInMs:       1000,        //流量控制器的独立统计结构的统计周期。如果StatIntervalInMs是1000，也就是统计QPS。
		},
	})
	if err != nil {
		fmt.Println(err)
		return
	}

	ch := make(chan struct{})
	for i := 0; i < 20; i++ {
		go func() {
			for {
				// 埋点逻辑，埋点资源名为 some-test
				e, b := sentinel.Entry("some-test")
				if b != nil {
					// 请求被拒绝，在此处进行处理
					fmt.Println(util.CurrentTimeMillis(), "Rejected", b)
					time.Sleep(time.Second)
				} else {
					// 请求允许通过，此处编写业务逻辑
					fmt.Println(util.CurrentTimeMillis(), "Passed")
					time.Sleep(time.Second)

					// 务必保证业务结束后调用 Exit
					e.Exit()
				}

			}
		}()
	}
	<-ch
}
