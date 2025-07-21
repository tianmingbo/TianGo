package main

import (
	"errors"
	"fmt"
	"sync"
)

// 事务ID，用于追踪整个分布式事务
type TxID string

// TCC核心接口，所有参与TCC事务的服务都需要实现此接口
type TCCService interface {
	// Try：资源检查与预留
	Try(txID TxID, params interface{}) error

	// Confirm：确认执行，真正执行业务逻辑
	Confirm(txID TxID) error

	// Cancel：取消操作，释放预留资源
	Cancel(txID TxID) error
}

// 事务状态
type TxStatus int

const (
	TxStatusInit      TxStatus = iota // 初始化
	TxStatusTrying                    // Try阶段中
	TxStatusConfirmed                 // 已确认
	TxStatusCancelled                 // 已取消
)

// 事务协调者，负责管理整个TCC事务流程
type Coordinator struct {
	services map[string]TCCService // 参与事务的服务
	txStatus map[TxID]TxStatus     // 事务状态记录
	mu       sync.RWMutex          // 保护事务状态的锁
}

// 创建新的协调者
func NewCoordinator() *Coordinator {
	return &Coordinator{
		services: make(map[string]TCCService),
		txStatus: make(map[TxID]TxStatus),
	}
}

// 注册参与TCC事务的服务
func (c *Coordinator) RegisterService(name string, service TCCService) {
	c.services[name] = service
}

// 执行TCC事务
func (c *Coordinator) ExecuteTx(txID TxID, paramsMap map[string]interface{}) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	// 检查事务是否已存在
	if _, exists := c.txStatus[txID]; exists {
		return errors.New("transaction already exists")
	}

	// 标记事务状态为初始化
	c.txStatus[txID] = TxStatusInit

	// 1. 执行所有服务的Try阶段
	c.txStatus[txID] = TxStatusTrying
	serviceNames := make([]string, 0, len(c.services))
	for name := range c.services {
		serviceNames = append(serviceNames, name)
	}

	for _, name := range serviceNames {
		service := c.services[name]
		params := paramsMap[name]

		// 执行Try操作
		if err := service.Try(txID, params); err != nil {
			// Try失败，执行所有已成功Try的服务的Cancel操作
			c.cancelTx(txID, serviceNames[:len(serviceNames)-1])
			return fmt.Errorf("service %s try failed: %v", name, err)
		}
	}

	// 2. 所有Try都成功，执行Confirm阶段
	if err := c.confirmTx(txID, serviceNames); err != nil {
		return fmt.Errorf("confirm transaction failed: %v", err)
	}

	return nil
}

// 确认事务
func (c *Coordinator) confirmTx(txID TxID, serviceNames []string) error {
	for _, name := range serviceNames {
		service := c.services[name]
		if err := service.Confirm(txID); err != nil {
			// 此处简化处理，实际中可能需要重试或人工干预
			return fmt.Errorf("service %s confirm failed: %v", name, err)
		}
	}

	c.txStatus[txID] = TxStatusConfirmed
	return nil
}

// 取消事务
func (c *Coordinator) cancelTx(txID TxID, serviceNames []string) error {
	// 反向执行Cancel，避免资源依赖问题
	for i := len(serviceNames) - 1; i >= 0; i-- {
		name := serviceNames[i]
		service := c.services[name]
		if err := service.Cancel(txID); err != nil {
			// 记录错误，但继续执行其他服务的Cancel
			fmt.Printf("warning: service %s cancel failed: %v\n", name, err)
		}
	}

	c.txStatus[txID] = TxStatusCancelled
	return nil
}

// 获取事务状态
func (c *Coordinator) GetTxStatus(txID TxID) TxStatus {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.txStatus[txID]
}
