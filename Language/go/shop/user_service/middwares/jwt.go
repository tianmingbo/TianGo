package middwares

import (
	"errors"
	"fmt"
	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
	"lGo/shop/user_service/global"
	"lGo/shop/user_service/models"
	"net/http"
)

func JWTAuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 从请求头中获取Authorization字段
		tokenString := c.GetHeader("Authorization")
		if tokenString == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header missing"})
			c.Abort()
			return
		}

		// 解析JWT
		claims := &models.Claims{}
		token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
			// 验证签名方法
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return []byte(global.Config.Server.JwtKey), nil
		})

		// 处理验证错误
		if err != nil {
			var ve *jwt.ValidationError
			if errors.As(err, &ve) {
				if ve.Errors&jwt.ValidationErrorMalformed != 0 {
					c.JSON(http.StatusUnauthorized, gin.H{"error": "token is malformed"})
				} else if ve.Errors&jwt.ValidationErrorExpired != 0 {
					c.JSON(http.StatusUnauthorized, gin.H{"error": "token is expired"})
				} else if ve.Errors&jwt.ValidationErrorNotValidYet != 0 {
					c.JSON(http.StatusUnauthorized, gin.H{"error": "token is not valid yet"})
				} else {
					c.JSON(http.StatusUnauthorized, gin.H{"error": "could not handle this token"})
				}
			}
			c.Abort()
			return
		}

		if !token.Valid {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "token is invalid"})
			c.Abort()
			return
		}

		// 验证通过，将claims信息存入上下文
		c.Set("claims", claims)
		c.Next()
	}
}
