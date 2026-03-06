package dao

import (
	"context"
	"database/sql"
	"errors"
	"time"

	"github.com/go-sql-driver/mysql"
	"gorm.io/gorm"
)

var (
	ErrUserDuplicateEmail = errors.New("邮箱冲突")
	ErrUserNotFound       = gorm.ErrRecordNotFound
)

//	type NullString struct {
//	   String string // 实际的字符串值
//	   Valid  bool   // 标记值是否有效（true=非NULL，false=NULL）
//	}

type User struct {
	ID       int64          `gorm:"primaryKey,autoIncrement"`
	Email    sql.NullString `gorm:"type:varchar(100);unique"`
	Phone    sql.NullString `gorm:"type:varchar(100);unique"`
	Password string
	NickName sql.NullString
	Birthday sql.NullString
	AboutMe  sql.NullString
	Ctime    int64 `gorm:"autoCreateTime:milli"`
	Utime    int64 `gorm:"autoCreateTime:milli"`
}

type GormUserDao struct {
	db *gorm.DB
}

func NewUserDao(db *gorm.DB) UserDao {
	return &GormUserDao{
		db: db,
	}
}

func (u *GormUserDao) Insert(ctx context.Context, user User) error {
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

func (u *GormUserDao) FindByEmail(ctx context.Context, email string) (User, error) {
	var user User
	err := u.db.WithContext(ctx).Where("email = ?", email).First(&user).Error
	return user, err
}

func (u *GormUserDao) UpdateById(ctx context.Context, user User) error {
	userId := ctx.Value("UserId")
	return u.db.WithContext(ctx).Where("id = ?", userId).Updates(&user).Error
}

func (u *GormUserDao) FindById(ctx context.Context) (User, error) {
	var user User
	userId := ctx.Value("UserId")
	err := u.db.WithContext(ctx).Where("id = ?", userId).First(&user).Error
	return user, err
}
