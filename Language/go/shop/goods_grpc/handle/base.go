package handle

import (
	"gorm.io/gorm"
	"lGo/shop/goods_grpc/proto"
)

type GoodsServer struct {
	proto.UnimplementedGoodsServer
}

func Paginate(page int, pageSize int) func(db *gorm.DB) *gorm.DB {
	return func(db *gorm.DB) *gorm.DB {
		switch {
		case pageSize > 100:
			pageSize = 100
		case pageSize <= 0:
			pageSize = 10
		}

		offset := (page - 1) * pageSize
		return db.Offset(offset).Limit(pageSize)
	}
}
