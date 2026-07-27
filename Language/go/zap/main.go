package main

import (
	"time"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// NewBusinessLogger 通用函数：创建指定业务的Logger
func NewBusinessLogger(business string) *zap.Logger {
	// 编码器配置（通用）
	encoderConfig := zapcore.EncoderConfig{
		TimeKey:    "time",
		LevelKey:   "level",
		MessageKey: "msg",
		CallerKey:  "caller",
		EncodeTime: func(t time.Time, enc zapcore.PrimitiveArrayEncoder) {
			enc.AppendString(t.Format("2006-01-02 15:04:05.000"))
		},
		EncodeLevel:  zapcore.CapitalLevelEncoder,
		EncodeCaller: zapcore.ShortCallerEncoder,
	}

	// 每个业务对应独立的日志文件
	logFile := "./logs/" + business + ".log"
	writer := zapcore.AddSync(&lumberjack.Logger{
		Filename:   logFile,
		MaxSize:    100,
		MaxBackups: 10,
		MaxAge:     7,
		Compress:   true,
	})

	// 创建Core
	core := zapcore.NewCore(
		zapcore.NewJSONEncoder(encoderConfig),
		writer,
		zapcore.InfoLevel,
	)

	// 构建Logger，并添加固定字段（标记业务）
	logger := zap.New(core, zap.AddCaller()).With(
		zap.String("business", business), // 所有日志自动带上业务标记
	)

	return logger
}

func main() {
	// 创建不同业务的Logger
	orderLogger := NewBusinessLogger("order")
	userLogger := NewBusinessLogger("user")
	payLogger := NewBusinessLogger("pay")

	// 确保刷入文件
	defer orderLogger.Sync()
	defer userLogger.Sync()
	defer payLogger.Sync()

	// 订单模块日志
	orderLogger.Info("订单创建",
		zap.String("order_id", "3001"),
		zap.Float64("amount", 99.9),
		zap.String("status", "pending"),
	)

	// 用户模块日志
	userLogger.Warn("用户密码过期",
		zap.String("user_id", "1001"),
		zap.Time("expire_time", time.Now().Add(-24*time.Hour)),
	)

	// 支付模块日志
	payLogger.Error("支付失败",
		zap.String("order_id", "3001"),
		zap.String("reason", "余额不足"),
		zap.Float64("balance", 10.5),
	)

	// 验证结果：
	// - 订单日志写入 ./logs/order.log
	// - 用户日志写入 ./logs/user.log
	// - 支付日志写入 ./logs/pay.log
}
