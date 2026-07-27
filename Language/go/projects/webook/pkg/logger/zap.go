package logger

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"gopkg.in/natefinch/lumberjack.v2"
)

type zapLogger struct {
	inner *zap.Logger
}

func (l *zapLogger) Debug(msg string, args ...any) {
	l.inner.Debug(msg, toZapFields(args...)...)
}

func (l *zapLogger) Debugf(format string, args ...any) {
	l.inner.Debug(fmt.Sprintf(format, args...))
}

func (l *zapLogger) Info(msg string, args ...any) {
	l.inner.Info(msg, toZapFields(args...)...)
}

func (l *zapLogger) Infof(format string, args ...any) {
	l.inner.Info(fmt.Sprintf(format, args...))
}

func (l *zapLogger) Warn(msg string, args ...any) {
	l.inner.Warn(msg, toZapFields(args...)...)
}

func (l *zapLogger) Warnf(format string, args ...any) {
	l.inner.Warn(fmt.Sprintf(format, args...))
}

func (l *zapLogger) Error(msg string, args ...any) {
	l.inner.Error(msg, toZapFields(args...)...)
}

func (l *zapLogger) Errorf(format string, args ...any) {
	l.inner.Error(fmt.Sprintf(format, args...))
}

func (l *zapLogger) Sync() error {
	return l.inner.Sync()
}

func toZapFields(args ...any) []zap.Field {
	if len(args) == 0 {
		return nil
	}

	fields := make([]zap.Field, 0, (len(args)+1)/2)
	for i := 0; i < len(args); i += 2 {
		if i+1 >= len(args) {
			fields = append(fields, zap.Any("arg", args[i]))
			continue
		}
		key := fmt.Sprint(args[i])
		fields = append(fields, zap.Any(key, args[i+1]))
	}

	return fields
}

// LoggerCfg 日志配置结构体
type LoggerCfg struct {
	Level      zapcore.Level // 日志级别
	Business   string        // 业务标识（会作为日志字段添加）
	MaxSize    int           // 单个日志文件最大大小(MB)
	MaxBackups int           // 最大备份文件数
	MaxAge     int           // 日志保留天数
	Compress   bool          // 是否压缩备份文件
	IsConsole  bool          // 是否输出到控制台（false则输出JSON格式到文件）
}

// LoggerOption 日志配置选项函数类型
type LoggerOption func(*LoggerCfg)

// WithLevel 设置日志级别
func WithLevel(level zapcore.Level) LoggerOption {
	return func(cfg *LoggerCfg) {
		cfg.Level = level
	}
}

// WithBusiness 设置业务标识（会添加到日志字段中）
func WithBusiness(business string) LoggerOption {
	return func(cfg *LoggerCfg) {
		cfg.Business = business
	}
}

// WithMaxSize 设置单个日志文件最大大小(MB)
func WithMaxSize(maxSize int) LoggerOption {
	return func(cfg *LoggerCfg) {
		if maxSize > 0 { // 防止无效值
			cfg.MaxSize = maxSize
		}
	}
}

// WithMaxBackups 设置日志备份文件最大数量
func WithMaxBackups(maxBackups int) LoggerOption {
	return func(cfg *LoggerCfg) {
		if maxBackups >= 0 { // 允许0（不限制），但建议生产环境设为>0
			cfg.MaxBackups = maxBackups
		}
	}
}

// WithMaxAge 设置日志文件最大保留天数
func WithMaxAge(maxAge int) LoggerOption {
	return func(cfg *LoggerCfg) {
		if maxAge > 0 {
			cfg.MaxAge = maxAge
		}
	}
}

// WithCompress 设置是否压缩备份文件
func WithCompress(compress bool) LoggerOption {
	return func(cfg *LoggerCfg) {
		cfg.Compress = compress
	}
}

// WithIsConsole 设置是否输出到控制台（true=控制台彩色格式，false=JSON文件格式）
func WithIsConsole(isConsole bool) LoggerOption {
	return func(cfg *LoggerCfg) {
		cfg.IsConsole = isConsole
	}
}

// NewLogger 创建Zap日志器
// path: 日志文件完整路径（如 "./logs/app.log"）
// opts: 可选配置项
func NewLogger(path string, opts ...LoggerOption) (Logger, error) {
	// 1. 初始化默认配置
	cfg := &LoggerCfg{
		Level:      zapcore.InfoLevel,
		Business:   "",
		MaxSize:    100,
		MaxBackups: 10,
		MaxAge:     7,
		Compress:   true,
		IsConsole:  true,
	}

	// 2. 应用自定义配置选项
	for _, opt := range opts {
		opt(cfg)
	}

	// 3. 配置日志编码器
	encoderCfg := zapcore.EncoderConfig{
		TimeKey:        "time",
		LevelKey:       "level",
		NameKey:        "logger",
		MessageKey:     "msg",
		CallerKey:      "caller",
		StacktraceKey:  "stacktrace",
		LineEnding:     zapcore.DefaultLineEnding,
		EncodeLevel:    zapcore.CapitalLevelEncoder,
		EncodeDuration: zapcore.SecondsDurationEncoder,
		EncodeCaller:   zapcore.ShortCallerEncoder,
		EncodeTime: func(t time.Time, enc zapcore.PrimitiveArrayEncoder) {
			enc.AppendString(t.Format("2006-01-02 15:04:05.000"))
		},
	}

	// 4. 按输出目标构建多 Core:
	// - 文件：固定 JSON，便于机器检索
	// - 控制台：彩色可读格式
	cores := make([]zapcore.Core, 0, 2)
	logPath := strings.TrimSpace(path)

	if logPath != "" {
		dir := filepath.Dir(logPath)
		if dir != "." && dir != "" {
			if err := os.MkdirAll(dir, 0o755); err != nil {
				return nil, fmt.Errorf("创建日志目录失败: %w", err)
			}
		}

		lumberjackLogger := &lumberjack.Logger{
			Filename:   logPath,
			MaxSize:    cfg.MaxSize,
			MaxBackups: cfg.MaxBackups,
			MaxAge:     cfg.MaxAge,
			Compress:   cfg.Compress,
			LocalTime:  true,
		}
		fileEncoderCfg := encoderCfg
		fileEncoderCfg.EncodeLevel = zapcore.CapitalLevelEncoder
		cores = append(cores, zapcore.NewCore(zapcore.NewJSONEncoder(fileEncoderCfg), zapcore.AddSync(lumberjackLogger), cfg.Level))
	}

	if cfg.IsConsole {
		consoleEncoderCfg := encoderCfg
		consoleEncoderCfg.EncodeLevel = zapcore.CapitalColorLevelEncoder
		cores = append(cores, zapcore.NewCore(zapcore.NewConsoleEncoder(consoleEncoderCfg), zapcore.AddSync(os.Stdout), cfg.Level))
	}

	if len(cores) == 0 {
		return nil, fmt.Errorf("日志输出目标为空: path 为空且未启用控制台输出")
	}

	// 5. 构建Logger（仅 Error 及以上打印堆栈，避免噪音）
	baseLogger := zap.New(
		zapcore.NewTee(cores...),
		zap.AddCaller(),                             // 显示调用文件和行号
		zap.AddStacktrace(zapcore.ErrorLevel),       // 仅Error级别以上输出堆栈
		zap.ErrorOutput(zapcore.AddSync(os.Stderr)), // 确保内部错误输出到标准错误
	)

	// 6. 如果设置了业务标识，添加固定字段
	if cfg.Business != "" {
		baseLogger = baseLogger.With(zap.String("business", cfg.Business))
	}

	return &zapLogger{inner: baseLogger}, nil
}
