package main

import (
	"crypto/md5"
	"encoding/hex"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"gorm.io/gorm/schema"
	"io"
	"log"
	"os"
	"time"

	"lGo/shop/goods_grpc/model"
)

func genMd5(code string) string {
	Md5 := md5.New()
	_, _ = io.WriteString(Md5, code)
	return hex.EncodeToString(Md5.Sum(nil))
}

func main() {
	dsn := "tian:Tian666~@tcp(124.222.56.172:3306)/goods?charset=utf8mb4&parseTime=True&loc=Local"

	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
		logger.Config{
			SlowThreshold: time.Second, // 慢 SQL 阈值
			LogLevel:      logger.Info, // Log level
			Colorful:      true,        // 禁用彩色打印
		},
	)

	// 全局模式
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
		NamingStrategy: schema.NamingStrategy{
			SingularTable: true,
		},
		Logger: newLogger,
	})
	if err != nil {
		panic(err)
	}

	_ = db.AutoMigrate(&model.Category{},
		&model.Brands{}, &model.GoodsCategoryBrand{}, &model.Banner{}, &model.Goods{})
	//Mysql2Es()
}

//func Mysql2Es() {
//	dsn := "root:root@tcp(192.168.0.104:3306)/mxshop_goods_srv?charset=utf8mb4&parseTime=True&loc=Local"
//
//	newLogger := logger.New(
//		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
//		logger.Config{
//			SlowThreshold: time.Second,   // 慢 SQL 阈值
//			LogLevel:      logger.Info, // Log level
//			Colorful:      true,         // 禁用彩色打印
//		},
//	)
//
//	// 全局模式
//	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
//		NamingStrategy: schema.NamingStrategy{
//			SingularTable: true,
//		},
//		Logger: newLogger,
//	})
//	if err != nil {
//		panic(err)
//	}
//
//	host := "http://192.168.0.104:9200"
//	logger := log.New(os.Stdout, "mxshop", log.LstdFlags)
//	global.EsClient, err = elastic.NewClient(elastic.SetURL(host), elastic.SetSniff(false),
//		elastic.SetTraceLog(logger))
//	if err != nil {
//		panic(err)
//	}
//
//	var goods []model.Goods
//	db.Find(&goods)
//	for _, g := range goods {
//		esModel := model.EsGoods{
//			ID:          g.ID,
//			CategoryID:  g.CategoryID,
//			BrandsID:    g.BrandsID,
//			OnSale:      g.OnSale,
//			ShipFree:    g.ShipFree,
//			IsNew:       g.IsNew,
//			IsHot:       g.IsHot,
//			Name:        g.Name,
//			ClickNum:    g.ClickNum,
//			SoldNum:     g.SoldNum,
//			FavNum:      g.FavNum,
//			MarketPrice: g.MarketPrice,
//			GoodsBrief:  g.GoodsBrief,
//			ShopPrice:   g.ShopPrice,
//		}
//
//		_, err = global.EsClient.Index().Index(esModel.GetIndexName()).BodyJson(esModel).Id(strconv.Itoa(int(g.ID))).Do(context.Background())
//		if err != nil {
//			panic(err)
//		}
//		//强调一下 一定要将docker启动es的java_ops的内存设置大一些 否则运行过程中会出现 bad request错误
//	}
//}
