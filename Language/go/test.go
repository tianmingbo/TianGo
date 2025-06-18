package main

import (
	"fmt"
	"github.com/spf13/viper"
	"log"
)

func initConfig() error {
	// 配置文件名称（不带扩展名）
	viper.SetConfigName("config")
	// 配置文件类型
	viper.SetConfigType("yaml")
	// 配置文件搜索路径
	viper.AddConfigPath(".") // 当前目录
	//viper.AddConfigPath("./config") // 配置子目录

	// 读取环境变量（可选）
	viper.AutomaticEnv()
	// 环境变量前缀（例如 APP_PORT 对应配置中的 app.port）
	viper.SetEnvPrefix("APP")

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// 配置文件不存在（可选处理）
			log.Println("配置文件未找到，使用默认值或环境变量")
		} else {
			// 配置文件存在但格式错误
			return fmt.Errorf("读取配置文件失败: %w", err)
		}
	}

	return nil
}

type Config struct {
	App struct {
		Name    string `mapstructure:"name"`
		Env     string `mapstructure:"env"`
		Port    int    `mapstructure:"port"`
		Timeout int    `mapstructure:"timeout"`
	} `mapstructure:"app"`

	Database struct {
		Host     string `mapstructure:"host"`
		Port     int    `mapstructure:"port"`
		User     string `mapstructure:"user"`
		Password string `mapstructure:"password"`
		DBName   string `mapstructure:"dbname"`
	} `mapstructure:"database"`

	Logging struct {
		Level  string `mapstructure:"level"`
		Format string `mapstructure:"format"`
		Output string `mapstructure:"output"`
	} `mapstructure:"logging"`
}

func main() {
	// 初始化配置
	if err := initConfig(); err != nil {
		log.Fatalf("初始化配置失败: %v", err)
	}

	//// 获取配置值
	//appName := viper.GetString("app.name")
	//appEnv := viper.GetString("app.env")
	//appPort := viper.GetInt("app.port")
	//
	//dbHost := viper.GetString("database.host")
	//dbPort := viper.GetInt("database.port")
	//dbUser := viper.GetString("database.user")
	////dbPassword := viper.GetString("database.password")
	//dbName := viper.GetString("database.dbname")
	//
	//// 打印配置
	//fmt.Printf("应用配置: %s (%s) running on port %d\n", appName, appEnv, appPort)
	//fmt.Printf("数据库连接: %s:%d/%s (user: %s)\n", dbHost, dbPort, dbName, dbUser)
	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		log.Fatalf("解析配置到结构体失败: %v", err)
	}
	fmt.Println(cfg.App)
	fmt.Println(cfg.Database)
	fmt.Println(cfg.Logging)

}
