package startup

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"webook/internal/repository/dao"
)

func InitDb() *gorm.DB {
	db, err := gorm.Open(mysql.Open("root:123456@tcp(10.6.64.191:3306)/webook?charset=utf8mb4&parseTime=True&loc=Local"), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	if err := dao.Init(db); err != nil {
		panic(err)
	}
	return db
}
