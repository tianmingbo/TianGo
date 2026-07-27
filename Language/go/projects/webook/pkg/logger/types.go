package logger

// Logger 抽象日志接口，方便替换为不同实现（zap/logrus/slog 等）
type Logger interface {
	Debug(msg string, args ...any)
	Debugf(format string, args ...any)
	Info(msg string, args ...any)
	Infof(format string, args ...any)
	Warn(msg string, args ...any)
	Warnf(format string, args ...any)
	Error(msg string, args ...any)
	Errorf(format string, args ...any)
	Sync() error
}
