package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"google.golang.org/protobuf/proto"

	"lGo/gin/pb"
)

type User struct {
	Name  string `json:"name"`
	Email string `json:"email"`
	Age   int    `json:"age"`
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

func createUser(c *gin.Context) {
	name := c.PostForm("name") //获取单个表单字段
	email := c.DefaultPostForm("email", "11@hotmail.com")
	auth := c.GetHeader("Authorization")    // 获取请求头
	session_id, _ := c.Cookie("session_id") // 获取 Cookie
	// 获取所有表单数据
	formData := make(map[string][]string)
	c.Request.ParseForm()
	formData = c.Request.PostForm

	//处理json数据, c.ShouldBind对于JSON, XML, MsgPack, ProtoBuf不能多次绑定
	// 1 绑定结构体
	var user User
	if err := c.ShouldBindBodyWith(&user, binding.JSON); err != nil {
		fmt.Println(err, "??")
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
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
		"session_id":    session_id,
		"name":          name,
		"email":         email,
		"all_form_data": formData,
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

func main() {
	router := gin.Default()
	router.GET("/ping", pong)
	api := router.Group("/api") //路由分组
	{
		api.GET("/users/:id", getUsers)
		api.POST("/users", createUser)
	}
	protobuf := router.Group("/protobuf")
	{
		protobuf.POST("/users", parseProtobuf)
	}
	router.Run() // 监听并在 0.0.0.0:8080 上启动服务
}
