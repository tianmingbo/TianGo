package main

import (
	"context"
	"fmt"

	"github.com/apache/rocketmq-client-go/v2/admin"
	"github.com/apache/rocketmq-client-go/v2/primitive"
)

func main() {
	topic := "newOne"
	//clusterName := "DefaultCluster"
	nameSrvAddr := []string{"10.6.64.191:9876"}
	brokerAddr := "10.6.64.191:10911"

	testAdmin, err := admin.NewAdmin(
		admin.WithResolver(primitive.NewPassthroughResolver(nameSrvAddr)),
		admin.WithCredentials(primitive.Credentials{
			AccessKey: "RocketMQ",
			SecretKey: "12345678",
		}),
	)

	// topic list
	result, err := testAdmin.FetchAllTopicList(context.Background())
	if err != nil {
		fmt.Println("FetchAllTopicList error:", err.Error())
	}
	fmt.Println(result.TopicList)

	//create topic
	err = testAdmin.CreateTopic(
		context.Background(),
		admin.WithTopicCreate(topic),
		admin.WithBrokerAddrCreate(brokerAddr),
	)
	if err != nil {
		fmt.Println("Create topic error:", err.Error())
	}

	//deletetopic
	err = testAdmin.DeleteTopic(
		context.Background(),
		admin.WithTopicDelete(topic),
		//admin.WithBrokerAddrDelete(brokerAddr),
		//admin.WithNameSrvAddr(nameSrvAddr),
	)
	if err != nil {
		fmt.Println("Delete topic error:", err.Error())
	}

	err = testAdmin.Close()
	if err != nil {
		fmt.Printf("Shutdown admin error: %s", err.Error())
	}
}
