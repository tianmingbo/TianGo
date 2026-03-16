package jwt

import "github.com/gin-gonic/gin"

type Jwt interface {
	ExtractToken(ctx *gin.Context) string
	SetJWTToken(ctx *gin.Context, userId int64, ssid string) error
	CheckSession(ctx *gin.Context, ssid string) error
	ClearToken(ctx *gin.Context) error
	SetLoginToken(ctx *gin.Context, userId int64) error
}
