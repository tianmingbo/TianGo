//go:build !k8s

//todo go:build dev
//todo go:build prod

package config

var Config = config{
	DB: DBConfig{
		DSN: "root:123456@tcp(10.6.64.191:3306)/webook",
	},
	Redis: RedisConfig{
		Addr:     "10.6.64.191:6389",
		Password: "tian666",
	},
}
