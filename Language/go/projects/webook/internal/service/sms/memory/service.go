package memory

import (
	"context"
	"fmt"
)

type Service struct {
}

func NewService() *Service {
	return &Service{}
}

func (s Service) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	fmt.Printf("code is %s\n", paramSet)
	return nil
}
