package handle

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"shop/global"
	model "shop/models"
	"shop/proto"
)

type UserServer struct {
	proto.UnimplementedUserServer
}

func page(users []model.User, pageNum int, size int) ([]model.User, error) {
	length := len(users)
	if length < pageNum*size+size {
		return users, nil
	} else {
		return users[pageNum*size : pageNum*size+size], nil
	}
}

func (u *UserServer) GetUserList(ctx context.Context, req *proto.PageInfo) (*proto.UserListResponse, error) {
	var users []model.User
	global.DB.Find(&users)

	var resp proto.UserListResponse
	resp.Total = int32(len(users))

	users, _ = page(users, int(req.Page), int(req.Size))

	return nil, status.Errorf(codes.Unimplemented, "method GetUserList not implemented")
}
func (u *UserServer) GetUserInfo(context.Context, *proto.IdRequest) (*proto.UserInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetUserInfo not implemented")
}
func (u *UserServer) GetUserMobile(context.Context, *proto.MobileRequest) (*proto.UserInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetUserMobile not implemented")
}
func (u *UserServer) CreateUser(context.Context, *proto.CreateUserReq) (*proto.UserInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateUser not implemented")
}
func (u *UserServer) UpdateUser(context.Context, *proto.UpdateUserReq) (*proto.Response, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateUser not implemented")
}
func (u *UserServer) CheckPassword(context.Context, *proto.CheckPasswordReq) (*proto.CheckPasswordResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CheckPassword not implemented")
}
