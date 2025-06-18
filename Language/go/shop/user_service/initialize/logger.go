package initialize

import (
	"fmt"
	"io"
	"os"
	"time"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"

	"lGo/shop/user_service/global"
)

func InitLogger() {
	writeSyncer := getLoggerWriter()
	encoder := getEncoder()
	core := zapcore.NewCore(encoder, writeSyncer, zap.DebugLevel) // 设置日志级别
	logger := zap.New(core, zap.AddCaller())
	zap.ReplaceGlobals(logger)
	zap.S().Infow("日志加载成功")
}

// getLoggerWriter 返回一个同步日志写入器。
func getLoggerWriter() zapcore.WriteSyncer {
	// 配置 Lumberjack logger 参数。
	lumberjackLogger := &lumberjack.Logger{
		Filename:   getLogName(), // 日志文件路径
		MaxSize:    10,           // 单个日志文件最大 size（MB）
		MaxBackups: 3,            // 保留的旧日志文件数量
		MaxAge:     7,            // 保留的旧日志文件最大天数
		Compress:   true,         // 是否压缩归档的日志文件
	}

	dest := io.MultiWriter(lumberjackLogger, os.Stdout)
	return zapcore.AddSync(dest)
}

// 配置编码器
func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	return zapcore.NewConsoleEncoder(encoderConfig)
}

func getLogName() string {
	now := time.Now().Format(time.DateOnly)
	return fmt.Sprintf("%s/%s.log", global.FileConfig.LogFile, now)
}
