package initialize

import (
	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/locales/en"
	"github.com/go-playground/locales/zh"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	en_translations "github.com/go-playground/validator/v10/translations/en"
	zh_translations "github.com/go-playground/validator/v10/translations/zh"
	"go.uber.org/zap"

	"lGo/shop/user_service/global"
)

func InitTranslator(local string) {
	//注册翻译器
	zhT := zh.New()
	enT := en.New()
	uni := ut.New(zhT, zhT, enT)

	global.Translator, _ = uni.GetTranslator(local)
	// 获取验证器引擎
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		switch local {
		case "zh":
			err := zh_translations.RegisterDefaultTranslations(v, global.Translator)
			if err != nil {
				zap.S().Errorf("init %s trans failed", local)
				return
			}
		case "en":
			err := en_translations.RegisterDefaultTranslations(v, global.Translator)
			if err != nil {
				zap.S().Errorf("init %s trans failed", local)
				return
			}
		default:
			zap.S().Errorf("not suppested %s", local)
			return

		}
	} else {
		panic("翻译器加载失败")
	}
	zap.S().Infow("翻译器加载成功")
	return
}
