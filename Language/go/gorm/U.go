package main

import (
	"gorm.io/gorm"
	"time"
)

// 钩子方法
func (u *User) BeforeUpdate(tx *gorm.DB) (err error) {
	u.UpdatedAt = time.Now() // 更新时间戳
	return nil
}

func main() {
	db := GetConnect()
	var user User
	db.First(&user)
	user.Name = "Tian"
	//更新单个记录
	db.Save(&user)

	//选择性更新字段
	db.Model(&User{ID: 2}).Update("name", "tian2") //更新单个字段
	db.Model(&User{ID: 2}).Updates(map[string]interface{}{
		"name":  "tian2.1",
		"age":   18,
		"email": "mb@gmail.com",
	}) //更新多个字段
	db.Model(&User{ID: 2}).Updates(&User{
		Name:  "tian2.1",
		Age:   0,
		Email: "mb@gmail.com",
	}) //更新多个字段,使用结构体更新不会使用0值

	//********批量更新*****
	db.Model(&User{}).Where("age > ?", 0).Updates(map[string]interface{}{
		"status": true,
	}) //默认禁止全局更新

	//********使用 SQL 表达式更新
	db.Model(&User{}).Where("id = ?", 1).Update("age", gorm.Expr("age + ?", 1)) // UPDATE `users` SET `age`=age + 1 WHERE id = 1

	// 使用子查询
	db.Model(&User{}).Where("id>1").Update("age", db.Select("id").First(&Order{}))

	//更新关联数据
	user2 := &User{
		ID:   1,
		Name: "Tian",
		Orders: []Order{
			{ID: 1, Amount: 1},
			{ID: 2, Amount: 2},
		},
	}
	db.Save(user2)
}
