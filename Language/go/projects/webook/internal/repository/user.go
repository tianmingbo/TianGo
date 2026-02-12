package repository

import (
	"context"
	"errors"
	"webook/internal/domain"
	"webook/internal/repository/cache"
	"webook/internal/repository/dao"
)

var (
	ErrUserDuplicateEmail = dao.ErrUserDuplicateEmail
	ErrUserNotFound       = dao.ErrUserNotFound
	ErrKeyNotExist        = cache.ErrKeyNotExist
)

type UserRepository struct {
	dao   *dao.UserDao
	cache *cache.UserCache
}

func NewUserRepository(dao *dao.UserDao, cache *cache.UserCache) *UserRepository {
	return &UserRepository{
		dao:   dao,
		cache: cache,
	}
}

func (r *UserRepository) CreateUser(ctx context.Context, u domain.User) error {
	return r.dao.Insert(ctx, dao.User{
		Email:    u.Email,
		Password: u.Password,
	})
}

func (r *UserRepository) FindByEmail(ctx context.Context, email string) (domain.User, error) {
	u, err := r.dao.FindByEmail(ctx, email)
	if err != nil {
		return domain.User{}, err
	}
	return domain.User{
		Id:       u.ID,
		Email:    u.Email,
		Password: u.Password,
	}, nil
}

func (r *UserRepository) UpdateById(ctx context.Context, u domain.User) error {
	return r.dao.UpdateById(ctx, dao.User{
		Phone:    u.Phone,
		NickName: u.Nickname,
		Birthday: u.Birthday,
		AboutMe:  u.AboutMe,
	})
}

func (r *UserRepository) FindById(ctx context.Context) (domain.User, error) {
	userId := ctx.Value("UserId")
	u, err := r.cache.Get(ctx, userId.(int64))
	if err == nil {
		return u, nil
	}
	//redis崩了，这里可能会把没数据库搞挂
	if errors.Is(err, ErrKeyNotExist) {
		ue, err := r.dao.FindById(ctx)
		if err != nil {
			return domain.User{}, err
		}
		u = domain.User{
			Id:       ue.ID,
			Email:    ue.Email,
			Phone:    ue.Phone,
			Nickname: ue.NickName,
			Birthday: ue.Birthday,
			AboutMe:  ue.AboutMe,
		}
		go func() { _ = r.cache.Set(ctx, u) }()
	}

	return domain.User{}, nil
}
