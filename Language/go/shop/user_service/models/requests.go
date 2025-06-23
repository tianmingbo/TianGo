package models

import (
	"github.com/dgrijalva/jwt-go"
)

type Claims struct {
	UserID   uint   `json:"user_id"`
	Username string `json:"username"`
	Role     uint   `json:"role"`
	jwt.StandardClaims
}
