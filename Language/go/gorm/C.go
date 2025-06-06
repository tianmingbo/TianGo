package main

import (
	"fmt"
	"gorm.io/gorm/clause"
	"log"
	"math/rand"
	"time"

	"gorm.io/gorm"
)

func generateRandomUsers(count int) []User {
	rand.Seed(time.Now().UnixNano())
	users := make([]User, count)
	names := []string{"Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
		"Kevin", "Linda", "Mike", "Nancy", "Oscar", "Patty", "Quinn", "Ryan", "Sally", "Tom"}

	for i := 0; i < count; i++ {
		name := names[rand.Intn(len(names))]
		age := rand.Intn(50) + 18
		email := fmt.Sprintf("%s%d@example.com", name, rand.Intn(1000))

		users[i] = User{
			ID:    uint(i) + 1,
			Name:  name,
			Age:   age,
			Email: email,
			Orders: []Order{
				{Amount: 100 * i},
				{Amount: 100*i + 1},
			},
		}
	}

	return users
}

func saveUsersToDB(db *gorm.DB, users []User) (error, int64) {
	if err := db.Exec("DELETE FROM users").Error; err != nil {
		return err, 0
	}
	if err := db.Exec("ALTER TABLE users AUTO_INCREMENT = 1").Error; err != nil {
		return err, 0
	}
	res := db.Create(&users) // 传递切片的指针
	return res.Error, res.RowsAffected
}

// upsert操作
func upsertUsersToDB(db *gorm.DB, users []User) (error, int64) {
	//通过索引直接修改原始切片|使用指针循环
	for i := range users {
		(&users[i]).Name = "tian"
	}
	// INSERT INTO `users` (`name`,`age`,`email`,`id`) VALUES ('tian',30,'tian890@example.com',1) ON DUPLICATE KEY UPDATE `name`=VALUES(`name`),`age`=VALUES(`age`)
	res := db.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "id"}},                     // 冲突检测字段
		DoUpdates: clause.AssignmentColumns([]string{"name", "age"}), // 冲突时更新的字段
	}).Create(&users) // 批量插入数据
	return res.Error, res.RowsAffected
}

func main() {
	users := generateRandomUsers(20)
	fmt.Printf("生成了 %d 条用户数据\n", len(users))

	db := GetConnect()
	fmt.Println(users)
	if err, addCount := saveUsersToDB(db, users); err != nil {
		log.Fatalf("保存到数据库失败: %v", err)
	} else {
		fmt.Println("add:", addCount)
	}
	fmt.Println("用户数据已成功保存到数据库")

	if err, addCount := upsertUsersToDB(db, users); err != nil {
		log.Fatalf("upsert到数据库失败: %v", err)
	} else {
		fmt.Println("upsert:", addCount)
	}
}
