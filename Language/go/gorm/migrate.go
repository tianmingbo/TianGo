package main

import "fmt"

func main() {
	db := GetConnect()
	err := db.AutoMigrate(&User{})
	if err != nil {
		panic(err)
	}
	fmt.Println("migrate success")
	fmt.Println(db.Migrator().HasIndex(User{}, "Name"))
	fmt.Println(db.Migrator().HasIndex(User{}, "idx_name"))
	err = db.Migrator().DropIndex(&User{}, "Name") //删除索引
	if err != nil {
		return
	}
	err = db.Migrator().CreateIndex(&User{}, "idx_name")
	if err != nil {
		return
	}
}
