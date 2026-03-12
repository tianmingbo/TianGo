package failover

import (
	"context"
	"sync/atomic"
	"webook/internal/service/sms"
)

//实现连续n个超时，自动切换下一个

type TimeOutSMSService struct {
	svcs      []sms.Service //所有服务
	idx       uint32        //当前调用的服务的下标
	cnt       uint32        //连续几个超时了
	threshold uint32        //超时阈值
}

func NewTimeOutSMSService(svcs []sms.Service, threshold uint32) *TimeOutSMSService {
	return &TimeOutSMSService{
		svcs:      svcs,
		threshold: threshold,
	}
}

func (s *TimeOutSMSService) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	errCnt := atomic.LoadUint32(&s.cnt)
	svcIdx := atomic.LoadUint32(&s.idx)
	if errCnt >= s.threshold {
		newIdx := (svcIdx + 1) % uint32(len(s.svcs))
		if atomic.CompareAndSwapUint32(&s.idx, svcIdx, newIdx) {
			// 重置这个 cnt 计数
			atomic.StoreUint32(&s.cnt, 0)
		}
		svcIdx = newIdx
	}
	err := s.svcs[svcIdx].Send(ctx, tplId, paramSet, number...)
	switch err {
	case nil:
		atomic.StoreUint32(&s.cnt, 0)
		return nil
	case context.DeadlineExceeded:
		atomic.AddUint32(&s.cnt, 1)
	default:
		atomic.AddUint32(&s.cnt, 1)
	}
	return err

}
