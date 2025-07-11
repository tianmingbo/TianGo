package handle

import (
	"context"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	"lGo/shop/goods_grpc/global"
	"lGo/shop/goods_grpc/model"
	"lGo/shop/goods_grpc/proto"
)

func ModelToResponse(goods model.Goods) proto.GoodsInfoResponse {
	return proto.GoodsInfoResponse{
		Id:              goods.ID,
		CategoryId:      goods.CategoryID,
		Name:            goods.Name,
		GoodsSn:         goods.GoodsSn,
		ClickNum:        goods.ClickNum,
		SoldNum:         goods.SoldNum,
		FavNum:          goods.FavNum,
		MarketPrice:     goods.MarketPrice,
		ShopPrice:       goods.ShopPrice,
		GoodsBrief:      goods.GoodsBrief,
		ShipFree:        goods.ShipFree,
		GoodsFrontImage: goods.GoodsFrontImage,
		IsNew:           goods.IsNew,
		IsHot:           goods.IsHot,
		OnSale:          goods.OnSale,
		DescImages:      goods.DescImages,
		Images:          goods.Images,
		Category: &proto.CategoryBriefInfoResponse{
			Id:   goods.Category.ID,
			Name: goods.Category.Name,
		},
		Brand: &proto.BrandInfoResponse{
			Id:   goods.Brands.ID,
			Name: goods.Brands.Name,
			Logo: goods.Brands.Logo,
		},
	}
}

func (g *GoodsServer) GoodsList(ctx context.Context, req *proto.GoodsFilterRequest) (*proto.GoodsListResponse, error) {
	var goods []model.Goods
	sql := "select * from goods where 1=1"
	var args []interface{}

	if req.PriceMin > 0 {
		sql += " and shop_price > ?"
		args = append(args, req.PriceMin)
	}
	if req.PriceMax > 0 {
		sql += " and shop_price < ?"
		args = append(args, req.PriceMin)
	}
	if req.IsHot {
		sql += " and is_hot =1"
	}
	if req.IsNew {
		sql += " and is_new=1"
	}
	if req.TopCategory > 0 {
		sql += " and category_id = ?"
		args = append(args, req.TopCategory)
	}
	if req.KeyWords != "" {
		sql += " and name like ?"
		args = append(args, "%"+req.KeyWords+"%")
	}
	if req.Brand > 0 {
		sql += " and brands_id = ?"
		args = append(args, req.Brand)
	}
	if req.Pages > 0 && req.PagePerNums > 0 {
		sql += " limit ? offset ?"
		args = append(args, req.Pages*req.PagePerNums, req.PagePerNums)
	}
	if err := global.DB.Raw(sql, args...).Scan(&goods).Error; err != nil {
		return nil, err
	}
	res := proto.GoodsListResponse{}
	res.Total = int32(len(goods))

	var categories []model.Category
	var brands []model.Brands
	categoryInfos := make(map[int32]*model.Category)
	brandInfos := make(map[int32]*model.Brands)
	categoryIds := make([]int32, 0)
	brandIds := make([]int32, 0)

	for _, good := range goods {
		categoryIds = append(categoryIds, good.CategoryID)
		brandIds = append(brandIds, good.BrandsID)
	}

	global.DB.Find(&categories, categoryIds)
	global.DB.Find(&brands, brandIds)

	for _, category := range categories {
		categoryInfos[category.ID] = &category
	}
	for _, brand := range brands {
		brandInfos[brand.ID] = &brand
	}

	for _, good := range goods {
		if v, ok := categoryInfos[good.CategoryID]; ok {
			good.Category = model.Category{
				BaseModel: model.BaseModel{ID: good.CategoryID},
				Name:      v.Name,
			}
		}

		if v, ok := brandInfos[good.BrandsID]; ok {
			good.Brands = model.Brands{
				BaseModel: model.BaseModel{ID: good.BrandsID},
				Name:      v.Name,
				Logo:      v.Logo,
			}
		}

		goodsInfoResponse := ModelToResponse(good)
		res.Data = append(res.Data, &goodsInfoResponse)
	}
	return &res, nil
}
func (g *GoodsServer) BatchGetGoods(ctx context.Context, req *proto.BatchGoodsIdInfo) (*proto.GoodsListResponse, error) {
	var goods []model.Goods
	goodsListResponse := &proto.GoodsListResponse{}
	result := global.DB.Where("id in ?", req.Id).Find(&goods)
	for _, good := range goods {
		goodsInfoResponse := ModelToResponse(good)
		goodsListResponse.Data = append(goodsListResponse.Data, &goodsInfoResponse)
	}
	goodsListResponse.Total = int32(result.RowsAffected)
	return goodsListResponse, nil
}
func (g *GoodsServer) CreateGoods(ctx context.Context, req *proto.CreateGoodsInfo) (*proto.GoodsInfoResponse, error) {
	var category model.Category
	if result := global.DB.First(&category, req.CategoryId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "商品分类不存在")
	}

	var brand model.Brands
	if result := global.DB.First(&brand, req.BrandId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "品牌不存在")
	}
	goods := model.Goods{
		Brands:          brand,
		BrandsID:        brand.ID,
		Category:        category,
		CategoryID:      category.ID,
		Name:            req.Name,
		GoodsSn:         req.GoodsSn,
		MarketPrice:     req.MarketPrice,
		ShopPrice:       req.ShopPrice,
		GoodsBrief:      req.GoodsBrief,
		ShipFree:        req.ShipFree,
		Images:          req.Images,
		DescImages:      req.DescImages,
		GoodsFrontImage: req.GoodsFrontImage,
		IsNew:           req.IsNew,
		IsHot:           req.IsHot,
		OnSale:          req.OnSale,
	}

	tx := global.DB.Begin()
	result := tx.Save(&goods)
	if result.Error != nil {
		tx.Rollback()
		return nil, result.Error
	}
	tx.Commit()
	return &proto.GoodsInfoResponse{
		Id: goods.ID,
	}, nil
}

func (g *GoodsServer) DeleteGoods(ctx context.Context, req *proto.DeleteGoodsInfo) (*emptypb.Empty, error) {
	if result := global.DB.Delete(&model.Goods{}, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "not found")
	}
	return &emptypb.Empty{}, nil
}

func (g *GoodsServer) UpdateGoods(ctx context.Context, req *proto.CreateGoodsInfo) (*emptypb.Empty, error) {
	var goods model.Goods

	if result := global.DB.First(&goods, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "商品不存在")
	}

	var category model.Category
	if result := global.DB.First(&category, req.CategoryId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "商品分类不存在")
	}

	var brand model.Brands
	if result := global.DB.First(&brand, req.BrandId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "品牌不存在")
	}

	goods.Brands = brand
	goods.BrandsID = brand.ID
	goods.Category = category
	goods.CategoryID = category.ID
	goods.Name = req.Name
	goods.GoodsSn = req.GoodsSn
	goods.MarketPrice = req.MarketPrice
	goods.ShopPrice = req.ShopPrice
	goods.GoodsBrief = req.GoodsBrief
	goods.ShipFree = req.ShipFree
	goods.Images = req.Images
	goods.DescImages = req.DescImages
	goods.GoodsFrontImage = req.GoodsFrontImage
	goods.IsNew = req.IsNew
	goods.IsHot = req.IsHot
	goods.OnSale = req.OnSale

	tx := global.DB.Begin()
	result := tx.Save(&goods)
	if result.Error != nil {
		tx.Rollback()
		return nil, result.Error
	}
	tx.Commit()
	return &emptypb.Empty{}, nil
}

func (g *GoodsServer) GetGoodsDetail(ctx context.Context, req *proto.GoodInfoRequest) (*proto.GoodsInfoResponse, error) {
	var goods model.Goods

	if result := global.DB.Preload("Category").Preload("Brands").First(&goods, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "商品不存在")
	}
	goodsInfoResponse := ModelToResponse(goods)
	return &goodsInfoResponse, nil
}
