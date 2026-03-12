package failover

import (
	"context"
	"sync"
	"sync/atomic"
	"time"
)

//错误率超过阈值切换

type req struct {
	reqTime time.Time
	isErr   bool
}

type FailRateSMSService struct {
	idx       uint32       // 当前使用的服务索引
	svcs      []SMSService // 短信服务列表
	threshold float64      // 错误率阈值（如0.3表示30%）
	reqs      []req        // 请求记录
	lock      sync.Mutex   // 保护reqs的锁
	windowSec int64        // 统计窗口（秒），比如10秒
	maxReqCnt int          // 最大记录数（防止内存无限增长）
}

func NewFailRateSMSService(svcs []SMSService, threshold float64, windowSec int64, maxReqCnt int) *FailRateSMSService {
	return &FailRateSMSService{
		svcs:      svcs,
		threshold: threshold,
		windowSec: windowSec,
		maxReqCnt: maxReqCnt,
	}
}

func (s *FailRateSMSService) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	// 1. 清理过期记录 + 限制最大记录数（加锁保证并发安全）
	s.lock.Lock()
	s.cleanExpiredReqs()
	// 限制最大记录数，避免内存泄漏
	if len(s.reqs) > s.maxReqCnt {
		s.reqs = s.reqs[len(s.reqs)-s.maxReqCnt:] // 只保留最近maxReqCnt条
	}
	reqCnt := len(s.reqs)
	s.lock.Unlock()

	// 2. 计算错误率（仅当记录数足够时判断，避免小样本误判）
	if reqCnt >= 10 { // 至少10条记录才判断，可配置
		s.lock.Lock()
		errCnt := 0
		for _, r := range s.reqs {
			if r.isErr {
				errCnt++
			}
		}
		// 浮点除法计算错误率，避免整除问题
		errRate := float64(errCnt) / float64(reqCnt)
		s.lock.Unlock()

		// 错误率超过阈值，尝试切换服务
		if errRate > s.threshold {
			svcIdx := atomic.LoadUint32(&s.idx)
			newIdx := (svcIdx + 1) % uint32(len(s.svcs))
			// CAS 操作保证原子切换
			if atomic.CompareAndSwapUint32(&s.idx, svcIdx, newIdx) {
				s.lock.Lock()
				s.reqs = s.reqs[:0] // 清空当前服务的错误记录
				s.lock.Unlock()
			}
		}
	}
	// 3. 获取最新的服务索引（无论是否切换）
	svcIdx := atomic.LoadUint32(&s.idx)
	// 4. 调用第三方服务
	err := s.svcs[svcIdx].Send(ctx, tplId, paramSet, number...)

	// 5. 记录请求结果（合并锁逻辑，减少冗余）
	s.lock.Lock()
	defer s.lock.Unlock() // 用defer保证锁释放，避免漏解锁
	s.reqs = append(s.reqs, req{
		reqTime: time.Now(),
		isErr:   err != nil, // 简化判断：非nil即为错误（包含超时）
	})

	return err
}

// 清理过期的请求记录（仅保留windowSec秒内的记录）
func (s *FailRateSMSService) cleanExpiredReqs() {
	if len(s.reqs) == 0 {
		return
	}
	// 计算过期时间点
	expireTime := time.Now().Add(-time.Duration(s.windowSec) * time.Second)
	// 找到第一个未过期的索引
	keepIdx := 0
	for i, r := range s.reqs {
		if r.reqTime.After(expireTime) {
			keepIdx = i
			break
		}
	}
	// 保留未过期的记录（切片截断，底层数组会被GC回收）
	s.reqs = s.reqs[keepIdx:]
}
