package initialize

import (
	"github.com/gin-gonic/gin/binding"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	"go.uber.org/zap"
	"lGo/shop/user_service/global"
	myValidator "lGo/shop/user_service/validator"
)

var (
	validate *validator.Validate
	ok       bool
)

func InitValidator() {
	if validate, ok = binding.Validator.Engine().(*validator.Validate); !ok {
		zap.S().Infof("绑定自定义验证器失败")
		return
	}
	initPwdValidator()
	initMobileValidator()
}

func initPwdValidator() {
	err := validate.RegisterValidation("strongPassword", myValidator.PasswordValidator)
	if err != nil {
		return
	}
	err = validate.RegisterTranslation("strongPassword", global.Translator, func(ut ut.Translator) error {
		//翻译注册器
		return ut.Add("strongPassword", "{0} 验证失败!", true)
	}, func(ut ut.Translator, fe validator.FieldError) string {
		//翻译获取器
		t, _ := ut.T("strongPassword", fe.Field())
		return t
	})
	if err != nil {
		zap.S().Error("注册验证器失败")
		return
	}
	zap.S().Info("strongPassword 验证器注册成功")
}

func initMobileValidator() {
	err := validate.RegisterValidation("mobile", myValidator.MobileValidator)
	if err != nil {
		return
	}
	err = validate.RegisterTranslation("mobile", global.Translator, func(ut ut.Translator) error {
		//翻译注册器
		return ut.Add("mobile", "{0} 验证失败!", true)
	}, func(ut ut.Translator, fe validator.FieldError) string {
		//翻译获取器
		t, _ := ut.T("mobile", fe.Field())
		return t
	})
	if err != nil {
		zap.S().Error("注册验证器失败")
		return
	}
	zap.S().Info("mobile 验证器注册成功")
}
