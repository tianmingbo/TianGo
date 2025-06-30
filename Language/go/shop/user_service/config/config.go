package config

import "time"

type FileConfig struct {
	ConfigFile string
	LogFile    string
}

type RedisConfig struct {
	Addr         string        `mapstructure:"addr"`         // Redis 服务器地址
	Password     string        `mapstructure:"password"`     // 密码
	DB           int           `mapstructure:"db"`           // 数据库
	PoolSize     int           `mapstructure:"poolSize"`     // 连接池大小
	MinIdleConns int           `mapstructure:"minIdleConns"` // 最小空闲连接数
	MaxConnAge   time.Duration `mapstructure:"maxConnAge"`   // 连接最大存活时间
	IdleTimeout  time.Duration `mapstructure:"idleTimeout"`  // 空闲连接超时时间
	MaxRetries   int           `mapstructure:"maxRetries"`   // 最大重试次数
}
type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host"`
	Port int    `mapstructure:"port" json:"port"`
}

type Config struct {
	Server struct {
		Name   string   `mapstructure:"name"`
		Env    string   `mapstructure:"env"`
		Port   int      `mapstructure:"port"`
		JwtKey string   `mapstructure:"jwtKey"`
		Host   string   `mapstructure:"host"`
		Tags   []string `mapstructure:"tags" json:"tags"`
	} `mapstructure:"server"`
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
	RedisConfig `mapstructure:"redis"`
	ConsulInfo  ConsulConfig `mapstructure:"consul" json:"consul"`
}
