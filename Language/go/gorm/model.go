package main

type User struct {
	ID    uint   `gorm:"primary_key"`
	Name  string `gorm:"size:50;index:idx_name"`
	Age   int    `gorm:"default:0"`
	Email string `gorm:"size:255;unique"`
}
