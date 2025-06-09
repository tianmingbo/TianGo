package main

import "fmt"

//关联关系操作

func main() {
	db := GetConnect()
	//创建用户时关联 Profile
	user := User{
		Name: "Tian",
		Profile: Profile{
			Address: "SH",
			Phone:   "0123456789",
		},
	}
	db.Save(&user)

	//查询关联
	var user1 User
	db.Preload("Profile").First(&user1, 21)
	fmt.Println(user1, user1.Profile.Address)
	user1.Profile.Address = "BJ"
	db.Model(&user).Association("Profile").Replace(&user.Profile)
}
