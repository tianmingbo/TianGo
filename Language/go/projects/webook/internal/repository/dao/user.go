package dao

import (
	"context"
	"errors"
	"time"

	"github.com/go-sql-driver/mysql"
	"gorm.io/gorm"
)

var (
	ErrUserDuplicateEmail = errors.New("邮箱冲突")
	ErrUserNotFound       = gorm.ErrRecordNotFound
)

type User struct {
	ID       int64  `gorm:"primaryKey,autoIncrement"`
	Email    string `gorm:"unique"`
	Phone    string `gorm:"unique"`
	Password string
	NickName string
	Birthday string
	AboutMe  string
	Ctime    int64
	Utime    int64
}

type UserDao struct {
	db *gorm.DB
}

func NewUserDao(db *gorm.DB) *UserDao {
	return &UserDao{
		db: db,
	}
}

func (u *UserDao) Insert(ctx context.Context, user User) error {
	now := time.Now().UnixMilli()
	user.Ctime = now
	user.Utime = now
	err := u.db.WithContext(ctx).Create(&user).Error
	var mysqlErr *mysql.MySQLError
	if errors.As(err, &mysqlErr) {
		const uniqueConflictErrNo uint16 = 1062
		if mysqlErr.Number == uniqueConflictErrNo {
			return ErrUserDuplicateEmail
		}
	}
	return err
}

func (u *UserDao) FindByEmail(ctx context.Context, email string) (User, error) {
	var user User
	err := u.db.WithContext(ctx).Where("email = ?", email).First(&user).Error
	return user, err
}

func (u *UserDao) UpdateById(ctx context.Context, user User) error {
	userId := ctx.Value("UserId")
	return u.db.WithContext(ctx).Where("id = ?", userId).Updates(&user).Error
}

func (u *UserDao) FindById(ctx context.Context) (User, error) {
	var user User
	userId := ctx.Value("UserId")
	err := u.db.WithContext(ctx).Where("id = ?", userId).First(&user).Error
	return user, err
}
