package main

import (
	"errors"
	"fmt"
	"sync"
)

// 用户账户
type UserAccount struct {
	UserID  string
	Balance float64 // 账户余额
	Frozen  float64 // 冻结金额（TCC Try阶段锁定）
	Paid    float64 // 已支付金额（TCC Confirm阶段确认）
	mu      sync.RWMutex
}

// 支付服务
type PaymentService struct {
	accounts map[string]*UserAccount // 用户账户，实际中会用数据库
	mu       sync.RWMutex
}

func NewPaymentService() *PaymentService {
	return &PaymentService{
		accounts: make(map[string]*UserAccount),
	}
}

// 支付参数
type PaymentParams struct {
	UserID string
	Amount float64
}

// 初始化用户账户
func (s *PaymentService) InitAccount(userID string, balance float64) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.accounts[userID] = &UserAccount{
		UserID:  userID,
		Balance: balance,
		Frozen:  0,
		Paid:    0,
	}
}

// Try：检查余额并冻结相应金额
func (s *PaymentService) Try(txID TxID, params interface{}) error {
	p, ok := params.(PaymentParams)
	if !ok {
		return errors.New("invalid params for payment service try")
	}

	s.mu.RLock()
	account, exists := s.accounts[p.UserID]
	s.mu.RUnlock()

	if !exists {
		return errors.New("user account not found")
	}

	account.mu.Lock()
	defer account.mu.Unlock()

	// 检查余额是否充足
	available := account.Balance - account.Frozen - account.Paid
	if available < p.Amount {
		return fmt.Errorf("insufficient balance for user %s, need %.2f, available %.2f",
			p.UserID, p.Amount, available)
	}

	// 冻结金额
	account.Frozen += p.Amount
	fmt.Printf("[PaymentService] Try success, txID: %s, user: %s, frozen: %.2f\n",
		txID, p.UserID, p.Amount)
	return nil
}

// Confirm：确认支付，将冻结金额转为实际支付
func (s *PaymentService) Confirm(txID TxID) error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	// 找到有冻结金额的账户并确认支付
	for _, account := range s.accounts {
		account.mu.Lock()
		if account.Frozen > 0 {
			frozen := account.Frozen
			account.Paid += frozen
			account.Frozen = 0
			account.mu.Unlock()
			fmt.Printf("[PaymentService] Confirm success, txID: %s, user: %s, paid: %.2f\n",
				txID, account.UserID, frozen)
			return nil
		}
		account.mu.Unlock()
	}

	return errors.New("no frozen amount found for confirm")
}

// Cancel：取消支付，解冻金额
func (s *PaymentService) Cancel(txID TxID) error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	// 找到有冻结金额的账户并解冻
	for _, account := range s.accounts {
		account.mu.Lock()
		if account.Frozen > 0 {
			frozen := account.Frozen
			account.Frozen = 0
			account.mu.Unlock()
			fmt.Printf("[PaymentService] Cancel success, txID: %s, user: %s, unfrozen: %.2f\n",
				txID, account.UserID, frozen)
			return nil
		}
		account.mu.Unlock()
	}

	return errors.New("no frozen amount found for cancel")
}

// 获取用户账户信息
func (s *PaymentService) GetAccount(userID string) (*UserAccount, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	account, exists := s.accounts[userID]
	return account, exists
}
