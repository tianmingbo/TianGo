package model

type Category struct {
	BaseModel
	Name             string      `gorm:"type:varchar(20);not null" json:"name"`
	ParentCategoryID int32       `json:"parent"`
	ParentCategory   *Category   `json:"-"`
	SubCategory      []*Category `gorm:"foreignKey:ParentCategoryID;references:ID" json:"sub_category"`
	Level            int32       `gorm:"type:int;not null;default:1" json:"level"`
	IsTab            bool        `gorm:"default:false;not null" json:"is_tab"`
}

func (Category) TableName() string {
	return "category"
}

type Brands struct {
	BaseModel
	Name string `gorm:"type:varchar(20);not null"`
	Logo string `gorm:"type:varchar(200);default:'';not null"`
}

type GoodsCategoryBrand struct {
	BaseModel
	CategoryID int32 `gorm:"type:int;index:idx_category_brand,unique"`
	Category   Category

	BrandsID int32 `gorm:"type:int;index:idx_category_brand,unique"`
	Brands   Brands
}

func (GoodsCategoryBrand) TableName() string {
	return "goodscategorybrand"
}

type Banner struct {
	BaseModel
	Image string `gorm:"type:varchar(200);not null"`
	Url   string `gorm:"type:varchar(200);not null"`
	Index int32  `gorm:"type:int;default:1;not null"`
}

type Goods struct {
	BaseModel

	CategoryID int32 `gorm:"type:int;not null"`
	Category   Category
	BrandsID   int32 `gorm:"type:int;not null"`
	Brands     Brands

	OnSale   bool `gorm:"default:false;not null"`
	ShipFree bool `gorm:"default:false;not null"`
	IsNew    bool `gorm:"default:false;not null"`
	IsHot    bool `gorm:"default:false;not null"`

	Name            string   `gorm:"type:varchar(50);not null"`
	GoodsSn         string   `gorm:"type:varchar(50);not null"`
	ClickNum        int32    `gorm:"type:int;default:0;not null"`
	SoldNum         int32    `gorm:"type:int;default:0;not null"`
	FavNum          int32    `gorm:"type:int;default:0;not null"`
	MarketPrice     float32  `gorm:"not null"`
	ShopPrice       float32  `gorm:"not null"`
	GoodsBrief      string   `gorm:"type:varchar(100);not null"`
	Images          GormList `gorm:"type:varchar(1000);not null"`
	DescImages      GormList `gorm:"type:varchar(1000);not null"`
	GoodsFrontImage string   `gorm:"type:varchar(200);not null"`
}

//func (g *Goods) AfterCreate(tx *gorm.DB) (err error){
//	esModel := EsGoods{
//		ID:          g.ID,
//		CategoryID:  g.CategoryID,
//		BrandsID:    g.BrandsID,
//		OnSale:      g.OnSale,
//		ShipFree:    g.ShipFree,
//		IsNew:       g.IsNew,
//		IsHot:       g.IsHot,
//		Name:        g.Name,
//		ClickNum:    g.ClickNum,
//		SoldNum:     g.SoldNum,
//		FavNum:      g.FavNum,
//		MarketPrice: g.MarketPrice,
//		GoodsBrief:  g.GoodsBrief,
//		ShopPrice:   g.ShopPrice,
//	}
//
//	_, err = global.EsClient.Index().Index(esModel.GetIndexName()).BodyJson(esModel).Id(strconv.Itoa(int(g.ID))).Do(context.Background())
//	if err != nil {
//		return err
//	}
//	return nil
//}

//func (g *Goods) AfterUpdate(tx *gorm.DB) (err error) {
//	esModel := EsGoods{
//		ID:          g.ID,
//		CategoryID:  g.CategoryID,
//		BrandsID:    g.BrandsID,
//		OnSale:      g.OnSale,
//		ShipFree:    g.ShipFree,
//		IsNew:       g.IsNew,
//		IsHot:       g.IsHot,
//		Name:        g.Name,
//		ClickNum:    g.ClickNum,
//		SoldNum:     g.SoldNum,
//		FavNum:      g.FavNum,
//		MarketPrice: g.MarketPrice,
//		GoodsBrief:  g.GoodsBrief,
//		ShopPrice:   g.ShopPrice,
//	}
//
//	_, err = global.EsClient.Update().Index(esModel.GetIndexName()).
//		Doc(esModel).Id(strconv.Itoa(int(g.ID))).Do(context.Background())
//	if err != nil {
//		return err
//	}
//	return nil
//}

//func (g *Goods) AfterDelete(tx *gorm.DB) (err error) {
//	_, err = global.EsClient.Delete().Index(EsGoods{}.GetIndexName()).Id(strconv.Itoa(int(g.ID))).Do(context.Background())
//	if err != nil {
//		return err
//	}
//	return nil
//}
