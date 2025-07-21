package main

import (
	"errors"
	"fmt"
	"sync"
)

// 订单状态
type OrderStatus string

const (
	OrderStatusPending   OrderStatus = "pending"   // 待确认
	OrderStatusConfirmed OrderStatus = "confirmed" // 已确认
	OrderStatusCancelled OrderStatus = "cancelled" // 已取消
)

// 订单
type Order struct {
	ID        string
	UserID    string
	ProductID string
	Quantity  int
	Amount    float64
	Status    OrderStatus
}

// 订单服务
type OrderService struct {
	orders map[string]*Order // 存储订单信息，实际中会用数据库
	mu     sync.RWMutex
}

func NewOrderService() *OrderService {
	return &OrderService{
		orders: make(map[string]*Order),
	}
}

// 创建订单参数
type CreateOrderParams struct {
	OrderID   string
	UserID    string
	ProductID string
	Quantity  int
	Amount    float64
}

// Try：创建订单并标记为待确认状态
func (s *OrderService) Try(txID TxID, params interface{}) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 参数校验
	p, ok := params.(CreateOrderParams)
	if !ok {
		return errors.New("invalid params for order service try")
	}

	// 检查订单是否已存在
	if _, exists := s.orders[p.OrderID]; exists {
		return errors.New("order already exists")
	}

	// 创建订单，状态为待确认
	s.orders[p.OrderID] = &Order{
		ID:        p.OrderID,
		UserID:    p.UserID,
		ProductID: p.ProductID,
		Quantity:  p.Quantity,
		Amount:    p.Amount,
		Status:    OrderStatusPending,
	}

	fmt.Printf("[OrderService] Try success, txID: %s, orderID: %s\n", txID, p.OrderID)
	return nil
}

// Confirm：确认订单，更新状态为已确认
func (s *OrderService) Confirm(txID TxID) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 实际中可以通过txID关联到具体订单，这里简化处理
	// 遍历所有订单找到属于当前事务的待确认订单
	for _, order := range s.orders {
		if order.Status == OrderStatusPending {
			order.Status = OrderStatusConfirmed
			fmt.Printf("[OrderService] Confirm success, txID: %s, orderID: %s\n", txID, order.ID)
			return nil
		}
	}

	return errors.New("no pending order found for confirm")
}

// Cancel：取消订单，更新状态为已取消
func (s *OrderService) Cancel(txID TxID) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 找到属于当前事务的待确认订单并取消
	for _, order := range s.orders {
		if order.Status == OrderStatusPending {
			order.Status = OrderStatusCancelled
			fmt.Printf("[OrderService] Cancel success, txID: %s, orderID: %s\n", txID, order.ID)
			return nil
		}
	}

	return errors.New("no pending order found for cancel")
}

// 获取订单
func (s *OrderService) GetOrder(orderID string) (*Order, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	order, exists := s.orders[orderID]
	return order, exists
}
