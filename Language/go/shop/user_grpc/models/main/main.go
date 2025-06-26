package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"

	"lGo/shop/models"
)

func GetConnect() *gorm.DB {
	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // 输出到控制台
		logger.Config{
			SlowThreshold: time.Second, // 慢 SQL 阈值
			LogLevel:      logger.Info, // 日志级别：Silent, Error, Warn, Info
			//IgnoreRecordNotFoundError: true,        // 忽略记录未找到错误
			ParameterizedQueries: false, // 禁用参数化查询，显示完整 SQL
		},
	)
	dsn := "tian:Tian666~@tcp(124.222.56.171)/gorm?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{Logger: newLogger})
	if err != nil {
		panic("failed to connect database")
	}
	fmt.Println("connect database success")
	return db
}

func main() {
	db := GetConnect()
	err := db.AutoMigrate(&model.User{})
	if err != nil {
		panic(err)
	}
}
