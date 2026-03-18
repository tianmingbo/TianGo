package jwt

import (
	"fmt"
	"net/http"
	"strings"
	"time"
	"webook/pkg/logger"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

var (
	AccessTokenKey  = []byte("pBMH@cKP65sknQI%ijB2DzhFnvsfiyt*")
	RefreshTokenKey = []byte("IfL$*Xhqa*RBij5j@zF9$x*bcN8lMSZc")
)

type RefreshClaims struct {
	UserId int64
	Ssid   string
	jwt.RegisteredClaims
}
type RedisJwt struct {
	cmd redis.Cmdable
	l   logger.Logger
}

func (r *RedisJwt) SetLoginToken(ctx *gin.Context, userId int64) error {
	ssid := uuid.New().String()
	err := r.SetJWTToken(ctx, userId, ssid)
	if err != nil {
		return err
	}
	err = r.SetRefreshToken(ctx, userId, ssid)
	return err
}
func (r *RedisJwt) SetRefreshToken(ctx *gin.Context, userId int64, ssid string) error {
	claims := RefreshClaims{
		UserId: userId,
		Ssid:   ssid,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Minute * 30)),
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenStr, err := token.SignedString(RefreshTokenKey)
	if err != nil {
		return err
	}
	r.l.Infof("refresh token generated, user_id=%d, ssid=%s", userId, ssid)
	ctx.Header("x-refresh-token", tokenStr)
	return nil
}

func (r *RedisJwt) ClearToken(ctx *gin.Context) error {
	// 退出登录将前端 header 设置为非法值
	ctx.Header("x-jwt-token", "")
	ctx.Header("x-refresh-token", "")

	claims := ctx.MustGet("cliams").(*UserClaims)
	return r.cmd.Set(ctx, fmt.Sprintf("users:ssid:%s", claims.Ssid), "", time.Hour*24*7).Err()
}
func NewRedisJwt(cmd redis.Cmdable, l logger.Logger) Jwt {
	return &RedisJwt{cmd: cmd, l: l}
}

func (r *RedisJwt) ExtractToken(ctx *gin.Context) string {
	authHeader := ctx.GetHeader("Authorization")
	if authHeader == "" {
		ctx.AbortWithStatus(http.StatusUnauthorized)
		return ""
	}

	parts := strings.SplitN(authHeader, " ", 2)
	if !(len(parts) == 2 && parts[0] == "Bearer") {
		ctx.AbortWithStatus(http.StatusUnauthorized)
		return ""
	}
	return parts[1]
}

type UserClaims struct {
	UserId    int64  `json:"userId"`
	Ssid      string `json:"ssid"`
	UserAgent string `json:"userAgent"`
	jwt.RegisteredClaims
}

func (r *RedisJwt) SetJWTToken(ctx *gin.Context, userId int64, ssid string) error {
	expirationTime := time.Now().Add(24 * time.Hour * 7)
	claims := &UserClaims{
		UserId:    userId,
		Ssid:      ssid,
		UserAgent: ctx.Request.UserAgent(),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenStr, err := token.SignedString(AccessTokenKey)
	if err != nil {
		return err
	}
	r.l.Infof("access token generated, user_id=%d, ssid=%s", userId, ssid)
	ctx.Header("x-jwt-token", tokenStr)
	return nil
}

func (r *RedisJwt) CheckSession(ctx *gin.Context, ssid string) error {
	_, err := r.cmd.Exists(ctx, fmt.Sprintf("users:ssid:%s", ssid)).Result()
	return err
}
