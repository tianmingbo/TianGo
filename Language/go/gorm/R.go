package main

import "fmt"

func main() {
	db := GetConnect()

	//var users []User
	var user User
	result := db.First(&user) //SELECT * FROM `users` ORDER BY `users`.`id` LIMIT 1
	fmt.Println(user, result.Error, result.RowsAffected)

	db.Take(&user)
	fmt.Println(user) //SELECT * FROM `users` WHERE `users`.`id` = 1 LIMIT 1

	db.Last(&user)
	fmt.Println(user) // SELECT * FROM `users` WHERE `users`.`id` = 1 ORDER BY `users`.`id` DESC LIMIT 1

	db.First(&user, "id=?", 10)
	fmt.Println(user)
}
