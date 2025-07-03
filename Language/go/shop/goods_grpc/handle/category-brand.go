package handle

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	"lGo/shop/goods_grpc/proto"
)

func (g *GoodsServer) CategoryBrandList(context.Context, *proto.CategoryBrandFilterRequest) (*proto.CategoryBrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CategoryBrandList not implemented")
}
func (g *GoodsServer) GetCategoryBrandList(context.Context, *proto.CategoryInfoRequest) (*proto.BrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetCategoryBrandList not implemented")
}
func (g *GoodsServer) CreateCategoryBrand(context.Context, *proto.CategoryBrandRequest) (*proto.CategoryBrandResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateCategoryBrand not implemented")
}
func (g *GoodsServer) DeleteCategoryBrand(context.Context, *proto.CategoryBrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteCategoryBrand not implemented")
}
func (g *GoodsServer) UpdateCategoryBrand(context.Context, *proto.CategoryBrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateCategoryBrand not implemented")
}
