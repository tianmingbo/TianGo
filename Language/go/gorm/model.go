package main

type User struct {
	ID     uint    `gorm:"primary_key"`
	Name   string  `gorm:"size:50;index:idx_name"`
	Age    int     `gorm:"default:0"`
	Email  string  `gorm:"size:255;unique"`
	Orders []Order // 一对多关联
}

type Order struct {
	ID     uint `gorm:"primary_key"`
	Amount int
	UserID uint //外键
}
