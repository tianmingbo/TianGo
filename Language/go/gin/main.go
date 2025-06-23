package main

import (
	"context"
	"errors"
	"fmt"
	"lGo/gin/global"
	"lGo/gin/middleware"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/locales/zh"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	zh_translations "github.com/go-playground/validator/v10/translations/zh"
	"google.golang.org/protobuf/proto"

	"lGo/gin/pb"
	"lGo/gin/validate"
)

type User struct {
	Name     string `json:"name" binding:"required"`
	Email    string `json:"email" binding:"omitempty,email"`
	Age      int    `json:"age" binding:"omitempty,min=1,max=130"`
	Password string `json:"password" binding:"omitempty,strongPassword"`
}

func pong(c *gin.Context) {
	c.AsciiJSON(200, gin.H{
		"lang": "GO语言",
		"tag":  "<br>"})
}
func getUsers(c *gin.Context) {
	id := c.Param("id")     //动态路由参数
	name := c.Query("name") //查询参数
	age := c.DefaultQuery("age", "18")
	all_query := c.Request.URL.Query()
	c.JSON(http.StatusOK, gin.H{"id": id, "name": name, "age": age, "all_query": all_query})
}

// 处理验证错误
func handleValidationError(c *gin.Context, err error) bool {
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
func createUser(c *gin.Context) {
	name := c.PostForm("name") //获取单个表单字段
	email := c.DefaultPostForm("email", "11@hotmail.com")
	auth := c.GetHeader("Authorization")   // 获取请求头
	sessionId, _ := c.Cookie("session_id") // 获取 Cookie
	// 获取所有表单数据
	formData := make(map[string][]string)
	c.Request.ParseForm()
	formData = c.Request.PostForm

	//处理json数据, c.ShouldBind对于JSON, XML, MsgPack, ProtoBuf不能多次绑定
	// 1 绑定结构体
	var user User
	if err := c.ShouldBindBodyWith(&user, binding.JSON); err != nil {
		//错误信息格式化
		handleValidationError(c, err)
		return
	}
	//2直接解析
	var jsonData map[string]interface{}
	if err := c.ShouldBindBodyWith(&jsonData, binding.JSON); err != nil {
		fmt.Println(err, "22")
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(201, gin.H{
		"auth":          auth,
		"form_name":     name,
		"form_email":    email,
		"session_id":    sessionId,
		"all_form_data": formData,
		"user":          user,
		"json_data":     jsonData,
	})
}

func parseProtobuf(c *gin.Context) {
	data, err := c.GetRawData()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "读取请求体失败"})
		return
	}

	// 解析 Protobuf 数据
	var req api.User
	if err := proto.Unmarshal(data, &req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "解析 Protobuf 失败: " + err.Error()})
		return
	}

	resp := &api.User{
		Id:     req.Id,
		Name:   req.Name,
		Email:  req.Email,
		Age:    req.Age,
		Gender: req.Gender,
	}

	// 序列化为 Protobuf 格式
	respData, err := proto.Marshal(resp)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "序列化 Protobuf 失败"})
		return
	}

	// 设置 Content-Type 并返回
	c.Data(http.StatusOK, "application/octet-stream", respData)
}

func initValidator() {
	// 获取验证器引擎
	v, ok := binding.Validator.Engine().(*validator.Validate)
	if !ok {
		fmt.Println("绑定自定义验证器失败")
	}

	err := v.RegisterValidation("strongPassword", validate.PasswordValidator)
	if err != nil {
		return
	}

	//注册翻译器
	zhT := zh.New()
	uni := ut.New(zhT, zhT)

	global.Translator, _ = uni.GetTranslator("zh")
	err = zh_translations.RegisterDefaultTranslations(v, global.Translator)
	if err != nil {
		fmt.Println("init trans failed")
	}

	err = v.RegisterTranslation("strongPassword", global.Translator, func(ut ut.Translator) error {
		//翻译注册器
		return ut.Add("strongPassword", "{0} 验证失败!", true)
	}, func(ut ut.Translator, fe validator.FieldError) string {
		//翻译获取器
		t, _ := ut.T("strongPassword", fe.Field())
		return t
	})
	if err != nil {
		fmt.Println("注册翻译器失败")
		return
	}
}

func main() {
	router := gin.Default()
	initValidator()
	router.GET("/ping", pong)
	v1 := router.Group("/api") //路由分组
	{
		v1.GET("/users/:id", getUsers)
		v1.POST("/users", middleware.Logger(), middleware.Auth(), createUser) //使用中间件
	}
	protobuf := router.Group("/protobuf")
	{
		protobuf.POST("/users", parseProtobuf)
	}
	//router.Run() 监听并在 0.0.0.0:8080 上启动服务

	srv := http.Server{
		Addr:    ":8080",
		Handler: router,
	}
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()
	log.Println("服务器已启动，监听端口 :8080")
	log.Println("按 Ctrl+C 优雅停止服务器...")

	s := make(chan os.Signal, 1)
	signal.Notify(s, syscall.SIGINT, syscall.SIGTERM) //注册信号处理器：将 SIGINT 和 SIGTERM 信号转发到 quit 通道。
	<-s                                               //读s

	log.Println("stopping")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("stopped failed:", err)
	}
	log.Println("stopped")
}
