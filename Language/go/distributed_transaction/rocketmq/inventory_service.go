package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/apache/rocketmq-client-go/v2/consumer"
	"github.com/apache/rocketmq-client-go/v2/primitive"
)

// Inventory 库存信息
type Inventory struct {
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"` // 当前库存数量
}

// 库存存储（实际应用中会使用数据库）
var inventoryStore = make(map[string]*Inventory)

// 库存消息处理器
type InventoryMessageHandler struct{}

func NewInventoryMessageHandler() *InventoryMessageHandler {
	return &InventoryMessageHandler{}
}

// 初始化库存
func (handler *InventoryMessageHandler) InitInventory(productID string, quantity int) {
	inventoryStore[productID] = &Inventory{
		ProductID: productID,
		Quantity:  quantity,
	}
	fmt.Printf("初始化产品 %s 库存: %d\n", productID, quantity)
}

// 获取库存
func (handler *InventoryMessageHandler) GetInventory(productID string) (*Inventory, error) {
	inventory, exists := inventoryStore[productID]
	if !exists {
		return nil, fmt.Errorf("产品 %s 库存不存在", productID)
	}
	return inventory, nil
}

// 处理订单消息，扣减库存
func (handler *InventoryMessageHandler) HandleMessage(ctx context.Context, msgs ...*primitive.MessageExt) (consumer.ConsumeResult, error) {
	for _, msg := range msgs {
		fmt.Printf("收到订单消息，消息ID: %s, 订单ID: %s\n", msg.MsgId, string(msg.Body))

		// 解析消息内容
		var orderParams OrderParams
		err := json.Unmarshal(msg.Body, &orderParams)
		if err != nil {
			fmt.Printf("解析消息失败: %v\n", err)
			// 消息解析失败，返回重试
			return consumer.ConsumeRetryLater, err
		}

		// 处理库存扣减
		err = handler.processInventoryDeduction(&orderParams)
		if err != nil {
			fmt.Printf("处理库存扣减失败: %v\n", err)
			// 处理失败，返回重试
			return consumer.ConsumeRetryLater, err
		}

		// 库存扣减成功，确认订单
		err = confirmOrder(orderParams.OrderID)
		if err != nil {
			fmt.Printf("确认订单失败: %v\n", err)
			// 确认订单失败，也返回成功，因为库存已经扣减，后续通过其他方式处理订单状态
			// 实际应用中可能需要更复杂的补偿机制
		}
	}

	// 所有消息处理成功
	return consumer.ConsumeSuccess, nil
}

// 处理库存扣减
func (handler *InventoryMessageHandler) processInventoryDeduction(orderParams *OrderParams) error {
	// 获取当前库存
	inventory, exists := inventoryStore[orderParams.ProductID]
	if !exists {
		return fmt.Errorf("产品 %s 库存不存在", orderParams.ProductID)
	}

	// 检查库存是否充足
	if inventory.Quantity < orderParams.Quantity {
		// 库存不足，取消订单
		cancelOrder(orderParams.OrderID)
		return fmt.Errorf("产品 %s 库存不足，当前: %d, 请求: %d",
			orderParams.ProductID, inventory.Quantity, orderParams.Quantity)
	}

	// 扣减库存
	inventory.Quantity -= orderParams.Quantity
	inventoryStore[orderParams.ProductID] = inventory
	fmt.Printf("产品 %s 库存扣减成功，扣减数量: %d, 剩余库存: %d\n",
		orderParams.ProductID, orderParams.Quantity, inventory.Quantity)

	return nil
}
