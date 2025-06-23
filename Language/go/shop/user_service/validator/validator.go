package validator

import (
	"github.com/go-playground/validator/v10"
	"regexp"
)

func PasswordValidator(fl validator.FieldLevel) bool {
	password := fl.Field().String()
	// 正则表达式：同时匹配大写字母、小写字母、数字，长度至少8位
	pattern := `\d{8}`
	match, _ := regexp.MatchString(pattern, password)
	return match
}

func MobileValidator(fl validator.FieldLevel) bool {
	password := fl.Field().String()
	pattern := `^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$`
	match, _ := regexp.MatchString(pattern, password)
	return match
}
