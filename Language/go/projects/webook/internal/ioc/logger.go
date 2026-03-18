package ioc

import (
	"os"
	"strconv"
	"webook/pkg/logger"
)

func InitLogger() logger.Logger {
	l, err := logger.NewZapLogger(logger.Config{
		Dir:         getEnv("LOG_DIR", "./logs"),
		DefaultFile: getEnv("LOG_FILE_APP", "app.log"),
		Files: map[string]string{
			"access":   getEnv("LOG_FILE_ACCESS", "access.log"),
			"security": getEnv("LOG_FILE_SECURITY", "security.log"),
			"sms":      getEnv("LOG_FILE_SMS", "sms.log"),
			"system":   getEnv("LOG_FILE_SYSTEM", "system.log"),
		},
		MaxSizeMB:  getEnvInt("LOG_MAX_SIZE_MB", 100),
		MaxBackups: getEnvInt("LOG_MAX_BACKUPS", 10),
		MaxAgeDays: getEnvInt("LOG_MAX_AGE_DAYS", 30),
		Compress:   getEnvBool("LOG_COMPRESS", true),
	})
	if err != nil {
		panic(err)
	}
	return l
}

func getEnv(key string, def string) string {
	v := os.Getenv(key)
	if v == "" {
		return def
	}
	return v
}

func getEnvInt(key string, def int) int {
	v := os.Getenv(key)
	if v == "" {
		return def
	}
	parsed, err := strconv.Atoi(v)
	if err != nil {
		return def
	}
	return parsed
}

func getEnvBool(key string, def bool) bool {
	v := os.Getenv(key)
	if v == "" {
		return def
	}
	parsed, err := strconv.ParseBool(v)
	if err != nil {
		return def
	}
	return parsed
}
