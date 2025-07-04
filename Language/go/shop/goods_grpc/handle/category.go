package handle

import (
	"context"
	"encoding/json"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
	"lGo/shop/goods_grpc/global"
	"lGo/shop/goods_grpc/model"
	"lGo/shop/goods_grpc/proto"
)

type treeNode struct {
	model.Category
	Children []*treeNode `json:"children"`
}

func getCategory1() (*proto.CategoryListResponse, error) {
	var categorys []model.Category
	res := proto.CategoryListResponse{}
	result := global.DB.Find(&categorys)
	res.Total = int32(result.RowsAffected)

	nodeMap := make(map[int32]*treeNode)
	for _, category := range categorys {
		nodeMap[category.ID] = &treeNode{
			Category: category,
			Children: make([]*treeNode, 0),
		}
	}

	var roots []*treeNode
	for _, node := range nodeMap {
		if node.ParentCategoryID == 0 {
			roots = append(roots, node)
		} else {
			if parent, ok := nodeMap[node.ParentCategoryID]; ok {
				parent.Children = append(parent.Children, node)
			}
		}
	}
	bytes, err := json.Marshal(roots)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "marshal json err: %v", err)
	}
	res.JsonData = string(bytes)
	return &res, nil
}

func getCategory2() (*proto.CategoryListResponse, error) {
	var categorys []model.Category
	global.DB.Where(&model.Category{Level: 1}).Preload("SubCategory.SubCategory").Find(&categorys)
	b, _ := json.Marshal(&categorys)
	return &proto.CategoryListResponse{JsonData: string(b)}, nil
}

func (g *GoodsServer) GetAllCategorysList(ctx context.Context, req *emptypb.Empty) (*proto.CategoryListResponse, error) {
	//return getCategory1()
	return getCategory2()
}
func (g *GoodsServer) GetSubCategory(ctx context.Context, req *proto.CategoryListRequest) (*proto.SubCategoryListResponse, error) {

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
