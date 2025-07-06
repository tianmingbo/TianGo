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

func (g *GoodsServer) CategoryBrandList(context.Context, *proto.CategoryBrandFilterRequest) (*proto.CategoryBrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CategoryBrandList not implemented")
}
func (g *GoodsServer) GetCategoryBrandList(context.Context, *proto.CategoryInfoRequest) (*proto.BrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetCategoryBrandList not implemented")
}

func (g *GoodsServer) CreateCategoryBrand(ctx context.Context, req *proto.CategoryBrandRequest) (*proto.CategoryBrandResponse, error) {
	var category model.Category
	if result := global.DB.First(&category, req.CategoryId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "not found category")
	}

	var brand model.Brands
	if result := global.DB.First(&brand, req.BrandId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.InvalidArgument, "not found brand")
	}
	categoryBrand := model.GoodsCategoryBrand{
		CategoryID: req.CategoryId,
		BrandsID:   req.BrandId,
	}
	global.DB.Save(&categoryBrand)
	return &proto.CategoryBrandResponse{Id: categoryBrand.ID}, nil
}

func (g *GoodsServer) DeleteCategoryBrand(ctx context.Context, req *proto.CategoryBrandRequest) (*emptypb.Empty, error) {
	if result := global.DB.Delete(&model.GoodsCategoryBrand{}, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "not found category brand")
	}
	return &emptypb.Empty{}, nil
}

func (g *GoodsServer) UpdateCategoryBrand(ctx context.Context, req *proto.CategoryBrandRequest) (*emptypb.Empty, error) {
	var categoryBrand model.GoodsCategoryBrand
	if result := global.DB.Find(&categoryBrand, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "not found category brand")
	}

	if result := global.DB.Find(&model.Category{}, req.CategoryId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "not found category")
	}

	if result := global.DB.Find(&model.Brands{}, req.BrandId); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "not found brand")
	}

	categoryBrand.CategoryID = req.CategoryId
	categoryBrand.BrandsID = req.BrandId
	global.DB.Save(&categoryBrand)
	return &emptypb.Empty{}, nil
}
