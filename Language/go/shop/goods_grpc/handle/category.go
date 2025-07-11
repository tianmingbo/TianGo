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

func getCategory1() (*proto.CategoryListResponse, error) {
	var categorys []model.Category
	res := proto.CategoryListResponse{}
	result := global.DB.Find(&categorys)
	res.Total = int32(result.RowsAffected)

	nodeMap := make(map[int32]*model.Category)
	for _, category := range categorys {
		nodeMap[category.ID] = &category
	}

	var roots []*model.Category
	for _, node := range nodeMap {
		if node.ParentCategoryID == 0 {
			roots = append(roots, node)
		} else {
			if parent, ok := nodeMap[node.ParentCategoryID]; ok {
				parent.SubCategory = append(parent.SubCategory, node)
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
	return getCategory1()
	//return getCategory2()
}
func (g *GoodsServer) GetSubCategory(ctx context.Context, req *proto.CategoryListRequest) (*proto.SubCategoryListResponse, error) {
	var categories []model.Category
	if result := global.DB.Where(req.Id).Or("parent_category_id = ?", req.Id).Find(&categories); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "category not found")
	}
	res := proto.SubCategoryListResponse{
		Total:        int32(len(categories)),
		SubCategorys: make([]*proto.CategoryInfoResponse, 0),
	}
	for _, category := range categories {
		if category.ParentCategoryID != req.Id {
			res.Info = &proto.CategoryInfoResponse{
				Id:             category.ID,
				Name:           category.Name,
				ParentCategory: category.ParentCategoryID,
				Level:          category.Level,
				IsTab:          category.IsTab,
			}
		} else {
			res.SubCategorys = append(res.SubCategorys, &proto.CategoryInfoResponse{
				Id:             category.ID,
				Name:           category.Name,
				ParentCategory: category.ParentCategoryID,
				Level:          category.Level,
				IsTab:          category.IsTab,
			})
		}
	}
	return &res, nil
}
func (g *GoodsServer) CreateCategory(ctx context.Context, req *proto.CategoryInfoRequest) (*proto.CategoryInfoResponse, error) {
	var category model.Category
	if result := global.DB.Where("name = ?", req.Name).First(&category); result.RowsAffected != 0 {
		return nil, status.Errorf(codes.InvalidArgument, "category name already exists")
	}
	category = model.Category{
		Name:             req.Name,
		ParentCategoryID: req.ParentCategory,
		Level:            req.Level,
		IsTab:            req.IsTab,
	}
	if result := global.DB.Create(&category); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.Internal, "insert failed")
	} else {
		return &proto.CategoryInfoResponse{Id: category.ID}, nil
	}
}

func (g *GoodsServer) DeleteCategory(ctx context.Context, req *proto.DeleteCategoryRequest) (*emptypb.Empty, error) {
	global.DB.Delete(&model.Category{}, req.Id)
	return &emptypb.Empty{}, nil
}
func (g *GoodsServer) UpdateCategory(ctx context.Context, req *proto.CategoryInfoRequest) (*emptypb.Empty, error) {
	var category model.Category
	if result := global.DB.First(&category, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "category not found")
	}
	if req.Name != "" {
		category.Name = req.Name
	}
	if req.ParentCategory != 0 {
		category.ParentCategoryID = req.ParentCategory
	}
	if req.Level != 0 {
		category.Level = req.Level
	}
	if req.IsTab {
		category.IsTab = req.IsTab
	}
	global.DB.Save(&category)
	return &emptypb.Empty{}, nil
}
