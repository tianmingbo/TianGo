package initialize

import (
	"fmt"
	"go.uber.org/zap"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"lGo/shop/user_grpc/global"
	"log"
	"os"
	"time"
)

func InitDB() {
	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // 输出到控制台
		logger.Config{
			SlowThreshold: time.Second, // 慢 SQL 阈值
			LogLevel:      logger.Info, // 日志级别：Silent, Error, Warn, Info
			//IgnoreRecordNotFoundError: true,        // 忽略记录未找到错误
			ParameterizedQueries: false, // 禁用参数化查询，显示完整 SQL
		},
	)
	c := global.Config.MysqlInfo
	fmt.Println(c)
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		c.User, c.Password, c.Host, c.Port, c.Name)
	var err error
	global.DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{Logger: newLogger})

	if err != nil {
		panic("failed to connect database")
	}
	zap.S().Info("connect database success")
}
