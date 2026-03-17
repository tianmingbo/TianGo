package main

// 根配置结构体（对应整个YAML文件）
type Config struct {
	Name   string `mapstructure:"name"`   // 对应yaml中的name字段
	Server Server `mapstructure:"server"` // 对应嵌套的server节点
	MySQL  MySQL  `mapstructure:"mysql"`  // 对应嵌套的mysql节点
	Redis  Redis  `mapstructure:"redis"`  // 对应嵌套的redis节点
}

// Server 配置（对应server节点）
type Server struct {
	Port       int      `mapstructure:"port"`        // 端口，int类型
	Debug      bool     `mapstructure:"debug"`       // 调试模式，bool类型
	AllowedIPs []string `mapstructure:"allowed_ips"` // 允许的IP列表，字符串切片
}

// MySQL 配置（对应mysql节点）
type MySQL struct {
	Host     string `mapstructure:"host"`     // 主机地址
	Port     int    `mapstructure:"port"`     // 端口
	User     string `mapstructure:"user"`     // 用户名
	Password string `mapstructure:"password"` // 密码
}

// Redis 配置（对应redis节点）
type Redis struct {
	Host     string `mapstructure:"host"`     // 主机地址
	Port     int    `mapstructure:"port"`     // 端口
	Password string `mapstructure:"password"` // 密码
	DB       int    `mapstructure:"db"`       // 数据库编号
}
