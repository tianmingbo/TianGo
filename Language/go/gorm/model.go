package main

import (
	"gorm.io/gorm"
	"time"
)

type Profile struct {
	gorm.Model
	UserID  uint // 外键
	Address string
	Phone   string
}
type User struct {
	ID        uint   `gorm:"primary_key"`
	Name      string `gorm:"size:50;index:idx_name"`
	Age       int    `gorm:"default:0"`
	Email     string `gorm:"size:255;unique"`
	Status    bool   `gorm:"default:false"`
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt // 软删除字段
	Orders    []Order        `gorm:"constraint:OnDelete:CASCADE"` // 级联删除, 一对多关联
	Profile   Profile        `gorm:"foreignKey:UserID"`           // 拥有一个 Profile
}

type Order struct {
	ID     uint `gorm:"primary_key"`
	Amount int
	UserID uint //外键
}
