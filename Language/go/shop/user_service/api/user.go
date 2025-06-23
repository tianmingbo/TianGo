package api

import (
	"context"
	"lGo/shop/user_service/forms"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"

	"lGo/shop/user_service/global"
	"lGo/shop/user_service/global/response"
	pb "lGo/shop/user_service/proto"
	"lGo/shop/user_service/utils"
)

func UserList(c *gin.Context) {
	page := c.DefaultQuery("page", "0")
	pageNum, _ := strconv.Atoi(page)
	size := c.DefaultQuery("size", "10")
	sizeNum, _ := strconv.Atoi(size)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	userList, err := global.UserClient.GetUserList(ctx, &pb.PageInfo{
		Page: uint32(pageNum),
		Size: uint32(sizeNum),
	})
	//错误处理
	if err != nil {
		zap.S().Errorw("[GetUserList] 查询 【用户列表】 失败", "msg", err.Error())
		utils.HandleGrpcErrorToHttpError(err, c)
		return
	}
	res := make([]interface{}, 0)
	for _, user := range userList.Data {
		userInfo := response.UserResponse{
			Id:       user.Id,
			Name:     user.NickName,
			Gender:   user.Gender,
			Birthday: user.BirthDay,
			Mobile:   user.Mobile,
		}
		res = append(res, userInfo)
	}
	c.JSON(http.StatusOK, res)
}

func PasswordLogin(c *gin.Context) {
	pwdForm := forms.PasswordLoginForm{}
	if err := c.ShouldBind(&pwdForm); err != nil {
		utils.HandleValidationError(c, err)
		return
	}
	userInfo, err := global.UserClient.GetUserMobile(context.Background(), &pb.MobileRequest{Mobile: pwdForm.Mobile})
	if err != nil {
		zap.S().Errorw("[PasswordLogin] 获取用户信息失败", "msg", err.Error())
		utils.HandleGrpcErrorToHttpError(err, c)
		return
	}

	checkRes, err := global.UserClient.CheckPassword(context.Background(), &pb.CheckPasswordReq{
		Password: pwdForm.Password,
		Id:       userInfo.Id,
	})
	if err != nil {
		zap.S().Errorw("[PasswordLogin] 验证密码失败", "msg", err.Error())
		utils.HandleGrpcErrorToHttpError(err, c)
		return
	}
	if !checkRes.IsValid {
		c.JSON(http.StatusBadRequest, gin.H{
			"code":    400,
			"message": "用户名或密码错误",
		})
		return
	} else {
		token, err := utils.GenerateToken(uint(userInfo.Id), userInfo.NickName, uint(userInfo.Role))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"code":    500,
				"message": "生成token失败",
			})
		}
		c.JSON(http.StatusOK, gin.H{
			"code":    200,
			"message": "登录成功",
			"token":   token,
		})
	}
}
