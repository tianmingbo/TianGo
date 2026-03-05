package dao

import (
	"context"
)

type UserDao interface {
	Insert(ctx context.Context, user User) error
	FindByEmail(ctx context.Context, email string) (User, error)
	UpdateById(ctx context.Context, user User) error
	FindById(ctx context.Context) (User, error)
}
