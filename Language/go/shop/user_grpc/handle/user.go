package handle

import (
	"context"
	"crypto/sha512"
	"encoding/hex"
	proto2 "lGo/shop/user_service/proto"
	"time"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"lGo/shop/user_grpc/global"
	model "lGo/shop/user_grpc/models"
)

type UserServer struct {
	proto2.UnimplementedUserServer
}

func page(users []model.User, pageNum int, size int) ([]model.User, error) {
	length := len(users)
	if length < pageNum*size+size {
		return users, nil
	} else {
		return users[pageNum*size : pageNum*size+size], nil
	}
}

func ModelToRsp(user model.User) *proto2.UserInfoResponse {
	birthday := ""
	if user.Birthday != nil {
		birthday = user.Birthday.Format(time.DateTime)
	}
	return &proto2.UserInfoResponse{
		Id:       user.ID,
		Mobile:   user.Mobile,
		NickName: user.NickName,
		BirthDay: birthday,
		Gender:   user.Gender,
		Role:     int32(user.Role),
	}
}

func encodePwd(pwd string) string {
	pwd = global.SECRET + pwd
	hash := sha512.Sum512([]byte(pwd))
	return hex.EncodeToString(hash[:])
}

func (u *UserServer) GetUserList(ctx context.Context, req *proto2.PageInfo) (*proto2.UserListResponse, error) {
	var users []model.User
	global.DB.Find(&users)

	var resp = &proto2.UserListResponse{}
	resp.Total = int32(len(users))

	users, _ = page(users, int(req.Page), int(req.Size))

	for _, v := range users {
		resp.Data = append(resp.Data, ModelToRsp(v))
	}
	return resp, nil
}
func (u *UserServer) GetUserInfo(ctx context.Context, req *proto2.IdRequest) (*proto2.UserInfoResponse, error) {
	var user model.User
	result := global.DB.First(&user, req.Id)
	if result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	var resp = &proto2.UserInfoResponse{}
	resp = ModelToRsp(user)
	return resp, nil
}
func (u *UserServer) GetUserMobile(ctx context.Context, req *proto2.MobileRequest) (*proto2.UserInfoResponse, error) {
	var user model.User
	res := global.DB.Where("mobile = ?", req.Mobile).First(&user)
	if res.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	return ModelToRsp(user), nil
}
func (u *UserServer) CreateUser(ctx context.Context, req *proto2.CreateUserReq) (*proto2.UserInfoResponse, error) {
	user := model.User{
		NickName: req.NickName,
		Mobile:   req.Mobile,
	}

	user.Password = encodePwd(req.Password)

	result := global.DB.Create(&user)
	if result.Error != nil {
		return nil, status.Errorf(codes.Internal, result.Error.Error())
	}
	return ModelToRsp(user), nil
}
func (u *UserServer) UpdateUser(ctx context.Context, req *proto2.UpdateUserReq) (*proto2.Response, error) {
	var user model.User
	if result := global.DB.First(&user, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	user.NickName = req.NickName
	user.Mobile = req.Mobile
	user.Password = encodePwd(req.Password)
	user.Gender = req.Gender
	user.Role = int(req.Role)
	if birthday, err := time.Parse(time.DateTime, req.BirthDay); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, err.Error())
	} else {
		user.Birthday = &birthday
	}

	if result := global.DB.Save(&user); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.Internal, result.Error.Error())
	}

	return &proto2.Response{Code: 200, Msg: "更新成功"}, nil
}
func (u *UserServer) CheckPassword(ctx context.Context, req *proto2.CheckPasswordReq) (*proto2.CheckPasswordResponse, error) {
	var user model.User
	if result := global.DB.First(&user, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	var resp = &proto2.CheckPasswordResponse{}
	resp.IsValid = false
	if encodePwd(req.Password) == user.Password {
		resp.IsValid = true
	}
	return resp, nil
}
