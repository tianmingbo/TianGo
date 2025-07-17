package main

import (
	"context"
	"log"
	_ "net/http/pprof"
	"time"

	"github.com/apache/rocketmq-client-go/v2"

	"github.com/apache/rocketmq-client-go/v2/rlog"

	"github.com/apache/rocketmq-client-go/v2/consumer"
	"github.com/apache/rocketmq-client-go/v2/primitive"
)

const (
	nameSrvAddr       = "http://10.6.64.191:9876"
	accessKey         = "rocketmq"
	secretKey         = "12345678"
	topic             = "test-topic"
	consumerGroupName = "testPullGroup"
	tag               = "testPull"
	namespace         = "ns"
)

var pullConsumer rocketmq.PullConsumer
var sleepTime = 1 * time.Second

func main() {
	rlog.SetLogLevel("info")
	var nameSrv, err = primitive.NewNamesrvAddr(nameSrvAddr)
	if err != nil {
		log.Fatalf("NewNamesrvAddr err: %v", err)
	}
	pullConsumer, err = rocketmq.NewPullConsumer(
		consumer.WithGroupName(consumerGroupName),
		consumer.WithNameServer(nameSrv),
		consumer.WithNamespace(namespace),
		consumer.WithMaxReconsumeTimes(2),
	)
	if err != nil {
		log.Fatalf("fail to new pullConsumer: %v", err)
	}

	// assign nil firstly to help consumer start up
	err = pullConsumer.Assign(topic, nil)
	if err != nil {
		log.Fatalf("fail to Assign: %v", err)
	}
	err = pullConsumer.Start()
	if err != nil {
		log.Fatalf("fail to Start: %v", err)
	}

	mqs, err := pullConsumer.GetTopicRouteInfo(topic)
	if err != nil {
		log.Fatalf("fail to GetTopicRouteInfo: %v", err)
	}

	for _, mq := range mqs {
		offset, err := pullConsumer.OffsetForTimestamp(mq, time.Now().UnixMilli()-60*10)
		if err != nil {
			log.Fatalf("fail to get offset for timestamp: %v", err)
		} else {
			pullConsumer.SeekOffset(mq, offset)
		}
	}

	err = pullConsumer.Assign(topic, mqs)
	if err != nil {
		log.Fatalf("fail to Assign: %v", err)
	}

	for {
		poll()
	}
}

func poll() {
	cr, err := pullConsumer.Poll(context.TODO(), time.Second*5)
	if consumer.IsNoNewMsgError(err) {
		log.Println("no new msg")
		return
	}
	if err != nil {
		log.Printf("[poll error] err=%v", err)
		time.Sleep(sleepTime)
		return
	}

	// todo LOGIC CODE HERE
	log.Println("msgList: ", cr.GetMsgList())
	log.Println("messageQueue: ", cr.GetMQ())
	log.Println("processQueue: ", cr.GetPQ())
	// pullConsumer.ACK(context.TODO(), cr, consumer.ConsumeRetryLater)
	pullConsumer.ACK(context.TODO(), cr, consumer.ConsumeSuccess)
}
