package main

import (
	"gorm.io/gorm"
	"time"
)

type Profile struct {
	gorm.Model
	UserID  uint `gorm:"not null;unique"` // 外键，关联User，确保唯一性（一对一）
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
	//DeletedAt gorm.DeletedAt // 软删除字段
	Orders  []Order `gorm:"constraint:OnDelete:CASCADE"`                                    // 级联删除, 一对多关联
	Profile Profile `gorm:"foreignKey:UserID;constraint:OnUpdate:CASCADE,OnDelete:CASCADE"` // 拥有一个 Profile
	Roles   []Role  `gorm:"many2many:user_roles;"`
}

type Role struct {
	gorm.Model
	Name  string
	Users []User `gorm:"many2many:user_roles;"`
}

type Order struct {
	ID     uint `gorm:"primary_key"`
	Amount int
	UserID uint //外键
}
