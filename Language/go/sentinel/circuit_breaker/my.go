package main

import (
	"errors"
	"fmt"
	"sync"
	"time"
)

const (
	StateClosed   = "closed"   // 闭合状态：正常允许请求
	StateOpen     = "open"     // 打开状态：拒绝所有请求
	StateHalfOpen = "halfOpen" // 半打开状态：允许部分请求尝试
)

type CircuitBreaker struct {
	mutex               sync.Mutex
	state               string        // 当前状态
	failureCount        int           // 失败计数
	successCount        int           // 成功计数
	windowStartTime     time.Time     // 统计窗口开始时间
	windowDuration      time.Duration // 统计窗口时长
	failureThreshold    int           // 失败阈值
	errorRateThreshold  float64       // 错误率阈值
	openDuration        time.Duration // 打开状态持续时间
	halfOpenMaxRequests int           // 半打开状态允许的最大请求数
}

// NewCircuitBreaker 初始化
func NewCircuitBreaker() *CircuitBreaker {
	return &CircuitBreaker{
		state:               StateClosed,
		windowDuration:      10 * time.Second, // 10秒统计窗口
		failureThreshold:    5,                // 最少失败次数
		errorRateThreshold:  0.5,              // 50%错误率
		openDuration:        5 * time.Second,  // 打开状态持续5秒
		halfOpenMaxRequests: 3,                // 半打开状态最多3个请求
		windowStartTime:     time.Now(),
	}
}

// AllowRequest 判断请求是否允许执行
func (cb *CircuitBreaker) AllowRequest() bool {
	cb.mutex.Lock()
	defer cb.mutex.Unlock()

	cb.checkAndSwitchState()
	switch cb.state {
	case StateClosed:
		return true
	case StateOpen:
		return false
	case StateHalfOpen:
		totalRequests := cb.successCount + cb.failureCount
		return totalRequests < cb.halfOpenMaxRequests
	default:
		return false
	}
}

// RecordResult 记录请求结果（成功/失败）
func (cb *CircuitBreaker) RecordResult(success bool) {
	cb.mutex.Lock()
	defer cb.mutex.Unlock()
	if time.Since(cb.windowStartTime) > cb.windowDuration {
		cb.resetStats()
	}
	if success {
		cb.successCount++
	} else {
		cb.failureCount++
	}

	cb.checkAndSwitchState()
}
func (cb *CircuitBreaker) checkAndSwitchState() {
	switch cb.state {
	case StateClosed:
		//检查是否从StateClosed切换到StateOpen
		totalRequests := cb.failureCount + cb.successCount
		if totalRequests >= cb.failureThreshold {
			errorRate := float64(cb.failureCount / totalRequests)
			if errorRate > cb.errorRateThreshold {
				cb.state = StateOpen
				cb.windowStartTime = time.Now() //记录打开的时间
				fmt.Println("closed -> open")
			}
		}
	case StateOpen:
		// 检查是否需要从打开状态转为半打开状态
		if time.Since(cb.windowStartTime) > cb.openDuration {
			cb.state = StateHalfOpen
			cb.resetStats()
			fmt.Println("open -> halfOpen")
		}
	case StateHalfOpen:
		// 检查半打开状态下的请求结果
		totalRequests := cb.successCount + cb.failureCount
		fmt.Println(totalRequests, cb.successCount, cb.failureCount)
		if totalRequests >= cb.halfOpenMaxRequests {
			errorRate := float64(cb.failureCount / totalRequests)
			if errorRate > cb.errorRateThreshold {
				cb.state = StateOpen
				cb.windowStartTime = time.Now()
				fmt.Println("halfOpen -> open")
			} else {
				cb.state = StateClosed
				fmt.Println("halfOpen -> close")
			}
			cb.resetStats()
		}
	}
}

// 重置统计数据
func (cb *CircuitBreaker) resetStats() {
	cb.successCount = 0
	cb.failureCount = 0
	cb.windowStartTime = time.Now()
}
func (cb *CircuitBreaker) GetState() string {
	cb.mutex.Lock()
	defer cb.mutex.Unlock()
	return cb.state
}
func callService(cb *CircuitBreaker, fail bool) error {
	if !cb.AllowRequest() {
		return errors.New("circuit breaker is not allowed request")
	}
	time.Sleep(10 * time.Millisecond)
	if fail {
		cb.RecordResult(false)
		return errors.New("circuit breaker fail")
	} else {
		cb.RecordResult(true)
		return nil
	}
}
func main() {

	cb := NewCircuitBreaker()

	// 模拟一批请求，前10个请求失败，触发熔断
	fmt.Println("=== 第一阶段：连续失败的请求 ===")
	for i := 0; i < 10; i++ {
		err := callService(cb, true)
		if err != nil {
			fmt.Printf("请求 %d: %v, 当前状态: %s\n", i+1, err, cb.GetState())
		} else {
			fmt.Printf("请求 %d: 成功, 当前状态: %s\n", i+1, cb.GetState())
		}
		time.Sleep(500 * time.Millisecond)
	}

	// 模拟熔断状态下的请求
	fmt.Println("\n=== 第二阶段：熔断状态下的请求 ===")
	for i := 0; i < 5; i++ {
		err := callService(cb, false)
		if err != nil {
			fmt.Printf("请求 %d: %v, 当前状态: %s\n", i+11, err, cb.GetState())
		} else {
			fmt.Printf("请求 %d: 成功, 当前状态: %s\n", i+11, cb.GetState())
		}
		time.Sleep(500 * time.Millisecond)
	}

	// 等待熔断器进入半打开状态
	fmt.Println("\n=== 等待熔断器进入半打开状态 ===")
	time.Sleep(6 * time.Second)

	// 模拟半打开状态下的请求
	fmt.Println("\n=== 第三阶段：半打开状态下的请求 ===")
	for i := 0; i < 5; i++ {
		// 前2个成功，第3个失败
		fail := i >= 2
		err := callService(cb, fail)
		if err != nil {
			fmt.Printf("请求 %d: %v, 当前状态: %s\n", i+16, err, cb.GetState())
		} else {
			fmt.Printf("请求 %d: 成功, 当前状态: %s\n", i+16, cb.GetState())
		}
		time.Sleep(500 * time.Millisecond)
	}

	// 再次等待熔断器进入半打开状态
	fmt.Println("\n=== 再次等待熔断器进入半打开状态 ===")
	time.Sleep(6 * time.Second)

	// 模拟半打开状态下全部成功的请求
	fmt.Println("\n=== 第四阶段：半打开状态下全部成功的请求 ===")
	for i := 0; i < 6; i++ {
		err := callService(cb, false)
		if err != nil {
			fmt.Printf("请求 %d: %v, 当前状态: %s\n", i+21, err, cb.GetState())
		} else {
			fmt.Printf("请求 %d: 成功, 当前状态: %s\n", i+21, cb.GetState())
		}
		time.Sleep(500 * time.Millisecond)
	}
}
