package main

import (
	"context"
	"log"
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

const refreshPersistOffsetDuration = time.Second * 5

func main() {
	rlog.SetLogLevel("info")
	var nameSrv, err = primitive.NewNamesrvAddr(nameSrvAddr)
	if err != nil {
		log.Fatalf("NewNamesrvAddr err: %v", err)
	}
	pullConsumer, err = rocketmq.NewPullConsumer(
		consumer.WithGroupName(consumerGroupName),
		consumer.WithNameServer(nameSrv),
		consumer.WithCredentials(primitive.Credentials{
			AccessKey: accessKey,
			SecretKey: secretKey,
		}),
		consumer.WithNamespace(namespace),
		consumer.WithMaxReconsumeTimes(2),
	)
	if err != nil {
		log.Fatalf("fail to new pullConsumer: %v", err)
	}
	selector := consumer.MessageSelector{
		Type:       consumer.TAG,
		Expression: tag,
	}
	err = pullConsumer.Subscribe(topic, selector)
	if err != nil {
		log.Fatalf("fail to Subscribe: %v", err)
	}
	err = pullConsumer.Start()
	if err != nil {
		log.Fatalf("fail to Start: %v", err)
	}

	timer := time.NewTimer(refreshPersistOffsetDuration)
	go func() {
		for ; true; <-timer.C {
			err = pullConsumer.PersistOffset(context.TODO(), topic)
			if err != nil {
				log.Printf("[pullConsumer.PersistOffset] err=%v", err)
			}
			timer.Reset(refreshPersistOffsetDuration)
		}
	}()

	for i := 0; i <= 4; i++ {
		go func() {
			for {
				pull()
			}
		}()
	}
	// make current thread hold to see pull result. TODO should update here
	time.Sleep(10000 * time.Second)
}

func pull() {
	resp, err := pullConsumer.Pull(context.TODO(), 1)
	if err != nil {
		log.Printf("[pull error] err=%v", err)
		time.Sleep(sleepTime)
		return
	}
	switch resp.Status {
	case primitive.PullFound:
		log.Printf("[pull message successfully] MinOffset:%d, MaxOffset:%d, nextOffset: %d, len:%d\n", resp.MinOffset, resp.MaxOffset, resp.NextBeginOffset, len(resp.GetMessages()))
		var queue *primitive.MessageQueue
		if len(resp.GetMessages()) <= 0 {
			return
		}
		for _, msg := range resp.GetMessageExts() {
			// todo LOGIC CODE HERE
			queue = msg.Queue
			//log.Println(msg.Queue, msg.QueueOffset, msg.GetKeys(), msg.MsgId, string(msg.Body))
			log.Println(msg)
		}
		// update offset
		err = pullConsumer.UpdateOffset(queue, resp.NextBeginOffset)
		if err != nil {
			log.Printf("[pullConsumer.UpdateOffset] err=%v", err)
		}

	case primitive.PullNoNewMsg, primitive.PullNoMsgMatched:
		log.Printf("[no pull message]   next = %d\n", resp.NextBeginOffset)
		time.Sleep(sleepTime)
		return
	case primitive.PullBrokerTimeout:
		log.Printf("[pull broker timeout]  next = %d\n", resp.NextBeginOffset)

		time.Sleep(sleepTime)
		return
	case primitive.PullOffsetIllegal:
		log.Printf("[pull offset illegal] next = %d\n", resp.NextBeginOffset)
		return
	default:
		log.Printf("[pull error]  next = %d\n", resp.NextBeginOffset)
	}
}
