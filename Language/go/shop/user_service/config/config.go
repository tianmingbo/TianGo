package config

import "time"

type FileConfig struct {
	ConfigFile string
	LogFile    string
}

type RedisConfig struct {
	Addr         string        `mapstructure:"addr" json:"addr"`                 // Redis 服务器地址
	Password     string        `mapstructure:"password" json:"password"`         // 密码
	DB           int           `mapstructure:"db" json:"db"`                     // 数据库
	PoolSize     int           `mapstructure:"poolSize" json:"poolSize"`         // 连接池大小
	MinIdleConns int           `mapstructure:"minIdleConns" json:"minIdleConns"` // 最小空闲连接数
	MaxConnAge   time.Duration `mapstructure:"maxConnAge" json:"maxConnAge"`     // 连接最大存活时间
	IdleTimeout  time.Duration `mapstructure:"idleTimeout" json:"idleTimeout"`   // 空闲连接超时时间
	MaxRetries   int           `mapstructure:"maxRetries" json:"maxRetries"`     // 最大重试次数
}
type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host"`
	Port int    `mapstructure:"port" json:"port"`
}

type NacosConfig struct {
	Host      string `mapstructure:"host"`
	Port      uint64 `mapstructure:"port"`
	Namespace string `mapstructure:"namespace"`
	User      string `mapstructure:"user"`
	Password  string `mapstructure:"password"`
	DataId    string `mapstructure:"dataid"`
	Group     string `mapstructure:"group"`
}

type Config struct {
	Server struct {
		Name   string   `mapstructure:"name" json:"name"`
		Env    string   `mapstructure:"env" json:"env"`
		Port   int      `mapstructure:"port" json:"port"`
		JwtKey string   `mapstructure:"jwtKey" json:"jwtKey"`
		Host   string   `mapstructure:"host" json:"host"`
		Tags   []string `mapstructure:"tags" json:"tags"`
	} `mapstructure:"server" json:"server"`
	Database struct {
		Host     string `mapstructure:"host" json:"host"`
		Port     int    `mapstructure:"port" json:"port"`
		User     string `mapstructure:"user" json:"user"`
		Password string `mapstructure:"password" json:"password"`
		DBName   string `mapstructure:"dbname" json:"dbname"`
	} `mapstructure:"database" json:"database"`
	Logging struct {
		Level  string `mapstructure:"level" json:"level"`
		Format string `mapstructure:"format" json:"format"`
		Output string `mapstructure:"output" json:"output"`
	} `mapstructure:"logging" json:"logging"`
	RedisConfig `mapstructure:"redis" json:"redis"`
	ConsulInfo  ConsulConfig `mapstructure:"consul" json:"consul"`
}
