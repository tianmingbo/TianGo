package handle

import (
	"context"
	"crypto/sha512"
	"encoding/hex"
	"time"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	"lGo/shop/global"
	model "lGo/shop/models"
	"lGo/shop/proto"
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

func ModelToRsp(user model.User) *proto.UserInfoResponse {
	birthday := ""
	if user.Birthday != nil {
		birthday = user.Birthday.Format(time.DateTime)
	}
	return &proto.UserInfoResponse{
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

func (u *UserServer) GetUserList(ctx context.Context, req *proto.PageInfo) (*proto.UserListResponse, error) {
	var users []model.User
	global.DB.Find(&users)

	var resp = &proto.UserListResponse{}
	resp.Total = int32(len(users))

	users, _ = page(users, int(req.Page), int(req.Size))

	for _, v := range users {
		resp.Data = append(resp.Data, ModelToRsp(v))
	}
	return resp, nil
}
func (u *UserServer) GetUserInfo(ctx context.Context, req *proto.IdRequest) (*proto.UserInfoResponse, error) {
	var user model.User
	result := global.DB.First(&user, req.Id)
	if result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	var resp = &proto.UserInfoResponse{}
	resp = ModelToRsp(user)
	return resp, nil
}
func (u *UserServer) GetUserMobile(ctx context.Context, req *proto.MobileRequest) (*proto.UserInfoResponse, error) {
	var user model.User
	res := global.DB.Where("mobile = ?", req.Mobile).First(&user)
	if res.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	return ModelToRsp(user), nil
}
func (u *UserServer) CreateUser(ctx context.Context, req *proto.CreateUserReq) (*proto.UserInfoResponse, error) {
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
func (u *UserServer) UpdateUser(ctx context.Context, req *proto.UpdateUserReq) (*proto.Response, error) {
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

	return &proto.Response{Code: 200, Msg: "更新成功"}, nil
}
func (u *UserServer) CheckPassword(ctx context.Context, req *proto.CheckPasswordReq) (*proto.CheckPasswordResponse, error) {
	var user model.User
	if result := global.DB.First(&user, req.Id); result.RowsAffected == 0 {
		return nil, status.Errorf(codes.NotFound, "用户不存在")
	}
	var resp = &proto.CheckPasswordResponse{}
	resp.IsValid = false
	if encodePwd(req.Password) == user.Password {
		resp.IsValid = true
	}
	return resp, nil
}
