package memory

import (
	"context"
	"fmt"
)

type Service struct {
}

func newService() *Service {
	return &Service{}
}

func (s Service) Send(ctx context.Context, tplId string, paramSet []string, number ...string) error {
	fmt.Printf("code is %s", paramSet)
	return nil
}
