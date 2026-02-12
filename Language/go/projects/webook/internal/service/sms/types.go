package sms

import "context"

type Service interface {
	Send(ctx context.Context, tplId string, paramSet []string, number ...string) error
}
