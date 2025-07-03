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

func getCategory1() (*proto.CategoryListResponse, error) {
	var categorys []model.Category
	res := proto.CategoryListResponse{}
	result := global.DB.Find(&categorys)
	res.Total = int32(result.RowsAffected)
	info := make(map[int32][]int32)
	for _, category := range categorys {
		if v, ok := info[category.ParentCategoryID]; ok {
			v = append(v, category.ID)
			info[category.ParentCategoryID] = v
		} else {
			info[category.ParentCategoryID] = []int32{category.ID}
		}
	}
	return &res, nil
}

//func getCategory2()(*proto.CategoryListResponse, error) {
//
//}

func (g *GoodsServer) GetAllCategorysList(context.Context, *emptypb.Empty) (*proto.CategoryListResponse, error) {
	return getCategory1()
}
func (g *GoodsServer) GetSubCategory(context.Context, *proto.CategoryListRequest) (*proto.SubCategoryListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetSubCategory not implemented")
}
func (g *GoodsServer) CreateCategory(context.Context, *proto.CategoryInfoRequest) (*proto.CategoryInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateCategory not implemented")
}
func (g *GoodsServer) DeleteCategory(context.Context, *proto.DeleteCategoryRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteCategory not implemented")
}
func (g *GoodsServer) UpdateCategory(context.Context, *proto.CategoryInfoRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateCategory not implemented")
}
