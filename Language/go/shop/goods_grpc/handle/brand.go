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

func (g *GoodsServer) BrandList(ctx context.Context, req *proto.BrandFilterRequest) (*proto.BrandListResponse, error) {
	res := &proto.BrandListResponse{}

	var total int64
	global.DB.Model(&model.Brands{}).Count(&total)
	res.Total = int32(total)

	var brands []model.Brands
	result := global.DB.Scopes(Paginate(int(req.Pages), int(req.PagePerNums))).Find(&brands)
	if result.Error != nil {
		return nil, result.Error
	}

	for _, v := range brands {
		brandInfo := proto.BrandInfoResponse{
			Id:   v.ID,
			Name: v.Name,
			Logo: v.Logo,
		}
		res.Data = append(res.Data, &brandInfo)
	}
	return res, nil
}

func (g *GoodsServer) CreateBrand(ctx context.Context, req *proto.BrandRequest) (*proto.BrandInfoResponse, error) {
	result := global.DB.Where("name = ?", req.Name).First(&model.Brands{})
	if result.RowsAffected != 0 {
		return nil, status.Errorf(codes.InvalidArgument, "品牌已存在")
	}
	brand := model.Brands{
		Name: req.Name,
		Logo: req.Logo,
	}
	global.DB.Create(&brand)
	return &proto.BrandInfoResponse{Id: brand.ID}, nil
}

func (g *GoodsServer) DeleteBrand(ctx context.Context, req *proto.BrandRequest) (*emptypb.Empty, error) {
	if result := global.DB.Delete(&model.Brands{}, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "品牌不存在")
	}
	return &emptypb.Empty{}, nil
}

func (g *GoodsServer) UpdateBrand(ctx context.Context, req *proto.BrandRequest) (*emptypb.Empty, error) {
	brand := model.Brands{}
	if result := global.DB.First(&brand, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "品牌不存在")
	}
	brand.Name = req.Name
	brand.Logo = req.Logo
	global.DB.Save(&brand)
	return &emptypb.Empty{}, nil
}
