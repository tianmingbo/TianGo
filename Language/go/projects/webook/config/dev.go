//go:build !k8s

//todo go:build dev
//todo go:build prod

package config

var Config = config{
	DB: DBConfig{
		DSN: "root:123456@tcp(127.0.0.1:3306)/webook",
	},
	Redis: RedisConfig{
		Addr:     "127.0.0.1:6379",
		Password: "123456",
	},
}
