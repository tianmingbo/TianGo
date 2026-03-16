package repository

import (
	"context"
	"database/sql"
	"errors"
	"webook/internal/domain"
	"webook/internal/repository/cache"
	"webook/internal/repository/cache/user"
	"webook/internal/repository/dao"
)

var (
	ErrUserDuplicate = dao.ErrUserDuplicate
	ErrUserNotFound  = dao.ErrUserNotFound
	ErrKeyNotExist   = user.ErrKeyNotExist
)

type CacheUserRepository struct {
	dao   dao.UserDao
	cache cache.UserCache
}

func NewUserRepository(dao dao.UserDao, cache cache.UserCache) UserRepository {
	return &CacheUserRepository{
		dao:   dao,
		cache: cache,
	}
}

func (r *CacheUserRepository) CreateUser(ctx context.Context, u domain.User) error {
	return r.dao.Insert(ctx, r.domainToEntity(u))
}

func (r *CacheUserRepository) FindByEmail(ctx context.Context, email string) (domain.User, error) {
	u, err := r.dao.FindByEmail(ctx, email)
	if err != nil {
		return domain.User{}, err
	}
	return domain.User{
		Id:       u.ID,
		Email:    u.Email.String,
		Password: u.Password,
	}, nil
}

func (r *CacheUserRepository) UpdateById(ctx context.Context, u domain.User) error {
	return r.dao.UpdateById(ctx, r.domainToEntity(u))
}

func (r *CacheUserRepository) FindById(ctx context.Context) (domain.User, error) {
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
			Email:    ue.Email.String,
			Phone:    ue.Phone.String,
			Nickname: ue.NickName.String,
			Birthday: ue.Birthday.String,
			AboutMe:  ue.AboutMe.String,
		}
		go func() { _ = r.cache.Set(ctx, u) }()
		return u, nil
	}

	return domain.User{}, nil
}

func (r *CacheUserRepository) FindByFeiShu(ctx context.Context, unionId string) (domain.User, error) {
	u, err := r.dao.FindByFeishu(ctx, unionId)
	if err != nil {
		return domain.User{}, err
	}
	return domain.User{
		Id:    u.ID,
		Email: u.Email.String,
		FeiShuInfo: domain.FeiShuInfo{
			UnionId: u.FeiShuUnionID.String,
		},
	}, nil
}

func (r *CacheUserRepository) domainToEntity(user domain.User) dao.User {
	return dao.User{
		ID: user.Id,
		Email: sql.NullString{
			String: user.Email,
			Valid:  user.Email != "",
		},
		Password: user.Password,
		Phone: sql.NullString{
			String: user.Phone,
			Valid:  user.Phone != "",
		},
		FeiShuUnionID: sql.NullString{
			String: user.FeiShuInfo.UnionId,
			Valid:  user.FeiShuInfo.UnionId != "",
		},
		NickName: sql.NullString{
			String: user.Nickname,
			Valid:  user.Nickname != "",
		},
		Birthday: sql.NullString{
			String: user.Birthday,
			Valid:  user.Birthday != "",
		},
		AboutMe: sql.NullString{
			String: user.AboutMe,
			Valid:  user.AboutMe != "",
		},
	}
}
