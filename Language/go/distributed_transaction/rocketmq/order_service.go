package main

import (
	"encoding/json"
	"fmt"

	"github.com/apache/rocketmq-client-go/v2/primitive"
)

// Order 订单信息
type Order struct {
	OrderID   string  `json:"order_id"`
	UserID    string  `json:"user_id"`
	ProductID string  `json:"product_id"`
	Quantity  int     `json:"quantity"`
	Amount    float64 `json:"amount"`
	Status    string  `json:"status"` // PENDING, CONFIRMED, CANCELED
}

// OrderParams 创建订单的参数
type OrderParams struct {
	OrderID   string
	UserID    string
	ProductID string
	Quantity  int
	Amount    float64
}

// 订单存储（实际应用中会使用数据库）
var orderStore = make(map[string]*Order)

// 订单事务监听器，实现TransactionListener接口
type OrderTransactionListener struct{}

func NewOrderTransactionListener() *OrderTransactionListener {
	return &OrderTransactionListener{}
}

// 执行本地事务
func (listener *OrderTransactionListener) ExecuteLocalTransaction(msg *primitive.Message) primitive.LocalTransactionState {
	// 解析消息中的订单参数
	var params OrderParams
	err := json.Unmarshal(msg.Body, &params)
	if err != nil {
		fmt.Printf("解析订单参数失败: %v\n", err)
		return primitive.RollbackMessageState
	}

	// 执行本地事务：创建订单（状态为待确认）
	fmt.Printf("执行本地事务，创建订单: %s\n", params.OrderID)
	order := &Order{
		OrderID:   params.OrderID,
		UserID:    params.UserID,
		ProductID: params.ProductID,
		Quantity:  params.Quantity,
		Amount:    params.Amount,
		Status:    "PENDING",
	}

	// 保存订单到存储
	orderStore[params.OrderID] = order

	// 这里可以添加其他本地事务逻辑，如扣减用户余额等

	// 本地事务执行成功，返回Commit状态
	return primitive.CommitMessageState
}

// 检查本地事务状态（用于RocketMQ回查）
func (listener *OrderTransactionListener) CheckLocalTransaction(msg *primitive.MessageExt) primitive.LocalTransactionState {
	// 解析消息中的订单参数
	var params OrderParams
	err := json.Unmarshal(msg.Body, &params)
	if err != nil {
		fmt.Printf("解析订单参数失败: %v\n", err)
		return primitive.RollbackMessageState
	}

	// 检查订单状态
	fmt.Printf("回查本地事务状态，订单: %s\n", params.OrderID)
	order, exists := orderStore[params.OrderID]
	if !exists {
		// 订单不存在，回滚消息
		fmt.Printf("订单 %s 不存在，回滚消息\n", params.OrderID)
		return primitive.RollbackMessageState
	}

	// 根据订单状态返回相应的事务状态
	switch order.Status {
	case "PENDING":
		// 订单仍为待确认状态，可能需要进一步处理
		// 这里可以根据业务逻辑判断是提交还是回滚
		return primitive.CommitMessageState
	case "CONFIRMED":
		// 订单已确认，提交消息
		return primitive.CommitMessageState
	case "CANCELED":
		// 订单已取消，回滚消息
		return primitive.RollbackMessageState
	default:
		return primitive.UnknowState
	}
}

// 构建订单消息
func BuildOrderMessage(orderID, userID, productID string, quantity int, amount float64) *primitive.Message {
	params := OrderParams{
		OrderID:   orderID,
		UserID:    userID,
		ProductID: productID,
		Quantity:  quantity,
		Amount:    amount,
	}

	body, _ := json.Marshal(params)
	msg := primitive.NewMessage("order_topic", body)
	msg.WithKeys([]string{orderID})

	return msg
}

// 确认订单
func confirmOrder(orderID string) error {
	order, exists := orderStore[orderID]
	if !exists {
		return fmt.Errorf("订单 %s 不存在", orderID)
	}

	order.Status = "CONFIRMED"
	orderStore[orderID] = order
	fmt.Printf("订单 %s 已确认\n", orderID)
	return nil
}

// 取消订单
func cancelOrder(orderID string) error {
	order, exists := orderStore[orderID]
	if !exists {
		return fmt.Errorf("订单 %s 不存在", orderID)
	}

	order.Status = "CANCELED"
	orderStore[orderID] = order
	fmt.Printf("订单 %s 已取消\n", orderID)
	return nil
}
