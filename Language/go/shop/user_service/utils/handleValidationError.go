package utils

import (
	"errors"
	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"lGo/shop/user_service/global"
	"net/http"
)

func HandleValidationError(c *gin.Context, err error) bool {
	if err == nil {
		return false
	}

	var ve validator.ValidationErrors
	if errors.As(err, &ve) {
		rsp := make(map[string]string)

		for _, fieldError := range ve {
			// 获取翻译后的错误消息
			rsp[fieldError.Field()] = fieldError.Translate(global.Translator)
		}

		c.JSON(http.StatusBadRequest, gin.H{
			"code":    400,
			"message": "参数验证失败",
			"rsp":     rsp,
		})

		return true
	}

	c.JSON(http.StatusBadRequest, gin.H{
		"code":    400,
		"message": "请求格式错误",
		"error":   err.Error(),
	})

	return true
}
