package utils

import (
	"time"

	"github.com/dgrijalva/jwt-go"

	"lGo/shop/user_service/global"
	"lGo/shop/user_service/models"
)

// GenerateToken 生成JWT
func GenerateToken(id uint, username string, role uint) (string, error) {
	// 创建声明
	expirationTime := time.Now().Add(24 * time.Hour * 30)
	claims := &models.Claims{
		UserID:   id,
		Username: username,
		Role:     role,
		StandardClaims: jwt.StandardClaims{
			// 过期时间
			ExpiresAt: expirationTime.Unix(),
			// 发行时间
			IssuedAt: time.Now().Unix(),
			// 发行人
			Issuer: "user_service",
		},
	}
	// 创建令牌对象，指定签名方法
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	// 使用密钥签名令牌
	return token.SignedString([]byte(global.Config.Server.JwtKey))
}
