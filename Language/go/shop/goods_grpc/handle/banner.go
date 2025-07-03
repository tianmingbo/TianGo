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

func (g *GoodsServer) BannerList(ctx context.Context, req *emptypb.Empty) (*proto.BannerListResponse, error) {
	res := &proto.BannerListResponse{}

	var total int64
	global.DB.Model(&model.Banner{}).Count(&total)
	res.Total = int32(total)

	var banners []model.Banner
	result := global.DB.Find(&banners)
	if result.Error != nil {
		return nil, result.Error
	}

	for _, v := range banners {
		brandInfo := proto.BannerResponse{
			Id:    v.ID,
			Index: v.Index,
			Image: v.Image,
			Url:   v.Url,
		}
		res.Data = append(res.Data, &brandInfo)
	}
	return res, nil
}
func (g *GoodsServer) CreateBanner(ctx context.Context, req *proto.BannerRequest) (*proto.BannerResponse, error) {

	banner := model.Banner{
		Index: req.Index,
		Image: req.Image,
		Url:   req.Url,
	}
	global.DB.Create(&banner)
	return &proto.BannerResponse{Id: banner.ID}, nil
}
func (g *GoodsServer) DeleteBanner(ctx context.Context, req *proto.BannerRequest) (*emptypb.Empty, error) {
	if result := global.DB.Delete(&model.Banner{}, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "品牌不存在")
	}
	return &emptypb.Empty{}, nil
}
func (g *GoodsServer) UpdateBanner(ctx context.Context, req *proto.BannerRequest) (*emptypb.Empty, error) {
	banner := model.Banner{}
	if result := global.DB.First(&banner, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "banner不存在")
	}
	banner.Index = req.Index
	banner.Image = req.Image
	banner.Url = req.Url

	global.DB.Save(&banner)
	return &emptypb.Empty{}, nil
}
