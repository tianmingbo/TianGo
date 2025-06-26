package utils

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/go-redis/redis/v8"
)

// Config 配置结构体
type Config struct {
	Addr         string        // Redis 服务器地址
	Password     string        // 密码
	DB           int           // 数据库
	PoolSize     int           // 连接池大小
	MinIdleConns int           // 最小空闲连接数
	MaxConnAge   time.Duration // 连接最大存活时间
	IdleTimeout  time.Duration // 空闲连接超时时间
	MaxRetries   int           // 最大重试次数
}

// RedisPool Redis 连接池结构体
type RedisPool struct {
	client *redis.Client
	config Config
	mu     sync.RWMutex
	closed bool
	stopCh chan struct{}
	wg     sync.WaitGroup
}

// NewRedisPool 创建一个新的 Redis 连接池
func NewRedisPool(config Config) (*RedisPool, error) {
	if config.PoolSize <= 0 {
		config.PoolSize = 10 // 默认连接池大小
	}

	if config.MinIdleConns <= 0 {
		config.MinIdleConns = 5 // 默认最小空闲连接数
	}

	if config.MaxConnAge <= 0 {
		config.MaxConnAge = 30 * time.Minute // 默认连接最大存活时间
	}

	if config.IdleTimeout <= 0 {
		config.IdleTimeout = 5 * time.Minute // 默认空闲连接超时时间
	}

	if config.MaxRetries < 0 {
		config.MaxRetries = 3 // 默认最大重试次数
	}

	client := redis.NewClient(&redis.Options{
		Addr:         config.Addr,
		Password:     config.Password,
		DB:           config.DB,
		PoolSize:     config.PoolSize,
		MinIdleConns: config.MinIdleConns,
		MaxConnAge:   config.MaxConnAge,
		IdleTimeout:  config.IdleTimeout,
		MaxRetries:   config.MaxRetries,
	})

	// 测试连接
	ctx := context.Background()
	_, err := client.Ping(ctx).Result()
	if err != nil {
		return nil, fmt.Errorf("连接 Redis 失败: %w", err)
	}

	pool := &RedisPool{
		client: client,
		config: config,
		stopCh: make(chan struct{}),
		closed: false,
	}

	// 启动连接监控协程
	pool.startConnectionMonitor()

	return pool, nil
}

// GetClient 获取 Redis 客户端
func (p *RedisPool) GetClient() *redis.Client {
	p.mu.RLock()
	defer p.mu.RUnlock()

	if p.closed {
		return nil
	}

	return p.client
}

// Close 关闭连接池
func (p *RedisPool) Close() error {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.closed {
		return nil
	}

	// 停止连接监控
	close(p.stopCh)
	p.wg.Wait()

	// 关闭客户端
	err := p.client.Close()
	p.closed = true

	return err
}

// startConnectionMonitor 启动连接监控协程
func (p *RedisPool) startConnectionMonitor() {
	p.wg.Add(1)
	go func() {
		defer p.wg.Done()

		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				p.checkConnections()
			case <-p.stopCh:
				return
			}
		}
	}()
}

// checkConnections 检查连接状态并尝试保持连接
func (p *RedisPool) checkConnections() {
	ctx := context.Background()

	// 检查连接是否正常
	_, err := p.client.Ping(ctx).Result()
	if err != nil {
		log.Printf("Redis 连接检查失败: %v，尝试重新连接...", err)

		// 尝试重置连接
		err = p.resetConnection()
		if err != nil {
			log.Printf("Redis 重新连接失败: %v", err)
		} else {
			log.Println("Redis 重新连接成功")
		}
	}
}

// resetConnection 重置 Redis 连接
func (p *RedisPool) resetConnection() error {
	p.mu.Lock()
	defer p.mu.Unlock()

	// 关闭当前客户端
	if !p.closed {
		err := p.client.Close()
		if err != nil {
			return fmt.Errorf("关闭旧 Redis 客户端失败: %w", err)
		}
	}

	// 创建新的客户端
	p.client = redis.NewClient(&redis.Options{
		Addr:         p.config.Addr,
		Password:     p.config.Password,
		DB:           p.config.DB,
		PoolSize:     p.config.PoolSize,
		MinIdleConns: p.config.MinIdleConns,
		MaxConnAge:   p.config.MaxConnAge,
		IdleTimeout:  p.config.IdleTimeout,
		MaxRetries:   p.config.MaxRetries,
	})

	// 测试新连接
	ctx := context.Background()
	_, err := p.client.Ping(ctx).Result()
	if err != nil {
		return fmt.Errorf("连接 Redis 失败: %w", err)
	}

	p.closed = false
	return nil
}
