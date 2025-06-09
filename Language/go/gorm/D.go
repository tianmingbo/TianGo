package main

import (
	"errors"
	"fmt"
	"gorm.io/gorm"
)

func (u *User) IsAdmin() bool {
	return u.ID == 1
}

// BeforeDelete 钩子
func (u *User) BeforeDelete(tx *gorm.DB) error {
	if u.IsAdmin() {
		return errors.New("admin user cannot be deleted")
	}
	return nil
}

func main() {
	db := GetConnect()

	//通过主键删除
	db.Delete(&User{ID: 1})

	//删除符合条件的多条记录
	db.Where("age > ?", 50).Delete(&User{})

	//批量删除
	db.Delete(&[]User{{ID: 3}, {ID: 4}})

	//软删除,如果有gorm.DeletedAt字段，自动获取软删除能力
	db.Delete(&User{ID: 2})

	//查询已删除记录
	var users []User
	db.Unscoped().Find(&users)
	fmt.Println(users)
	//只查询被删除的记录
	db.Unscoped().Where("deleted_at IS NOT NULL").Find(&users)
	fmt.Println(users)
}
