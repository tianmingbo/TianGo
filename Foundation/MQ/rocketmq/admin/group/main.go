package main

import (
	"context"
	"fmt"
	"time"

	"github.com/apache/rocketmq-client-go/v2/admin"
	"github.com/apache/rocketmq-client-go/v2/primitive"
)

func main() {
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

	// group list
	result, err := testAdmin.GetAllSubscriptionGroup(context.Background(), brokerAddr, 3*time.Second)
	if err != nil {
		fmt.Println("GetAllSubscriptionGroup error:", err.Error())
	}
	fmt.Println(result.SubscriptionGroupTable)

	err = testAdmin.Close()
	if err != nil {
		fmt.Printf("Shutdown admin error: %s", err.Error())
	}
}
