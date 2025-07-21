package main

import (
	"errors"
	"fmt"
	"sync"
)

// 库存项
type InventoryItem struct {
	ProductID string
	Total     int // 总库存
	Reserved  int // 已预留库存（TCC Try阶段锁定）
	Allocated int // 已分配库存（TCC Confirm阶段确认）
	mu        sync.RWMutex
}

// 库存服务
type InventoryService struct {
	inventory map[string]*InventoryItem // 产品库存，实际中会用数据库
	mu        sync.RWMutex
}

func NewInventoryService() *InventoryService {
	return &InventoryService{
		inventory: make(map[string]*InventoryItem),
	}
}

// 扣减库存参数
type DeductInventoryParams struct {
	ProductID string
	Quantity  int
}

// 初始化产品库存
func (s *InventoryService) InitInventory(productID string, quantity int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.inventory[productID] = &InventoryItem{
		ProductID: productID,
		Total:     quantity,
		Reserved:  0,
		Allocated: 0,
	}
}

// Try：检查库存并预留
func (s *InventoryService) Try(txID TxID, params interface{}) error {
	p, ok := params.(DeductInventoryParams)
	if !ok {
		return errors.New("invalid params for inventory service try")
	}

	s.mu.RLock()
	item, exists := s.inventory[p.ProductID]
	s.mu.RUnlock()

	if !exists {
		return errors.New("product not found in inventory")
	}

	item.mu.Lock()
	defer item.mu.Unlock()

	// 检查库存是否充足
	available := item.Total - item.Reserved - item.Allocated
	if available < p.Quantity {
		return fmt.Errorf("insufficient inventory for product %s, need %d, available %d",
			p.ProductID, p.Quantity, available)
	}

	// 预留库存
	item.Reserved += p.Quantity
	fmt.Printf("[InventoryService] Try success, txID: %s, product: %s, reserved: %d\n",
		txID, p.ProductID, p.Quantity)
	return nil
}

// Confirm：确认扣减库存，将预留转为实际分配
func (s *InventoryService) Confirm(txID TxID) error {
	// 实际中可以通过txID关联到具体的预留记录，这里简化处理
	s.mu.RLock()
	defer s.mu.RUnlock()

	// 找到有预留库存的商品并确认扣减
	for _, item := range s.inventory {
		item.mu.Lock()
		if item.Reserved > 0 {
			reserved := item.Reserved
			item.Allocated += reserved
			item.Reserved = 0
			item.mu.Unlock()
			fmt.Printf("[InventoryService] Confirm success, txID: %s, product: %s, allocated: %d\n",
				txID, item.ProductID, reserved)
			return nil
		}
		item.mu.Unlock()
	}

	return errors.New("no reserved inventory found for confirm")
}

// Cancel：取消库存预留，释放库存
func (s *InventoryService) Cancel(txID TxID) error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	// 找到有预留库存的商品并释放
	for _, item := range s.inventory {
		item.mu.Lock()
		if item.Reserved > 0 {
			reserved := item.Reserved
			item.Reserved = 0
			item.mu.Unlock()
			fmt.Printf("[InventoryService] Cancel success, txID: %s, product: %s, released: %d\n",
				txID, item.ProductID, reserved)
			return nil
		}
		item.mu.Unlock()
	}

	return errors.New("no reserved inventory found for cancel")
}

// 获取产品库存状态
func (s *InventoryService) GetInventory(productID string) (*InventoryItem, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	item, exists := s.inventory[productID]
	return item, exists
}
