package main

import "gorm.io/gorm/clause"

//关联关系操作

func main() {
	db := GetConnect()
	//创建用户时关联 Profile
	//user := User{
	//	Name: "Tian",
	//	Profile: Profile{
	//		Address: "SH",
	//		Phone:   "0123456789",
	//	},
	//}
	//db.Create(&user)
	//
	////查询关联
	//var user1 User
	//res := db.Preload("Profile").First(&user1, 1)
	//fmt.Println(res.Error)
	////更新关联
	////user1.Profile.Address = "BJ"
	////更新关联1
	////tx := db.Session(&gorm.Session{FullSaveAssociations: true}) //不使用FullSaveAssociations，只会更新user表
	////tx.Save(&user1)                                             // 使用FullSaveAssociations，会同时更新User和Profile表
	//
	////更新关联2
	//db.Save(&user1)         // 先保存主对象
	//db.Save(&user1.Profile) // 再单独保存关联对象
	////删除关联
	//db.Delete(&user1)
	//
	////*************一对多****************
	//user = User{
	//	Name:  "Tian",
	//	Email: "tian@gmail.com",
	//	Orders: []Order{
	//		{Amount: 100},
	//		{Amount: 200},
	//	},
	//}
	//db.Create(&user)
	//
	//var user2 User
	//db.Preload("Orders").First(&user2)
	//fmt.Println(user2.Orders)
	//
	//user2.Orders = append(user2.Orders, Order{Amount: 300})
	////db.Save(&user2)
	////db.Save(&user2.Orders)
	//
	//db.Session(&gorm.Session{FullSaveAssociations: true}).Save(&user2)
	//
	//db.Delete(&user2) // 需配合OnDelete:CASCADE约束

	//****************多对多******************
	// 创建（添加用户和角色）
	//adminRole := Role{Name: "Admin"}
	//userRole := Role{Name: "User"}
	//db.Create(&adminRole)
	//db.Create(&userRole)
	//
	//user3 := User{
	//	Name:  "Charlie",
	//	Roles: []Role{adminRole, userRole},
	//}
	//db.Create(&user3)

	// 查询（获取用户及其角色）
	var user4 User
	db.Preload("Roles").First(&user4, 1)
	//fmt.Println(user4.Roles)
	// 更新（添加新角色）
	editorRole := Role{Name: "Editor"}
	db.Create(&editorRole)
	db.Model(&user4).Association("Roles").Append(&editorRole)

	//删除（解除用户与角色的关联）
	db.Model(&user4).Association("Roles").Delete(&adminRole)

	// 删除用户 时，也删除用户的所有一对一、一对多和多对多关联
	db.Select(clause.Associations).Where("id>?", 1).Delete(&user4)
}
