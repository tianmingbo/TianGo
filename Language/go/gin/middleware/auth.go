package middleware

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

func Auth() gin.HandlerFunc {
	return func(c *gin.Context) {
		for k, v := range c.Request.Header {
			if k == "User-Agent" {
				if strings.Contains(strings.Join(v, ","), "Postman") {
					c.JSON(http.StatusUnauthorized, gin.H{"error": "认证失败"})

					//终止后续逻辑
					c.Abort()
				}
			}
		}
		c.Next()
	}
}
