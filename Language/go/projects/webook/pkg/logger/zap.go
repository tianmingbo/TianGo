package logger

import (
	"fmt"
	"os"
	"path/filepath"
	"sync"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"gopkg.in/natefinch/lumberjack.v2"
)

type Config struct {
	Dir         string
	DefaultFile string
	Files       map[string]string
	MaxSizeMB   int
	MaxBackups  int
	MaxAgeDays  int
	Compress    bool
}

type zapFactory struct {
	cfg     Config
	mu      sync.RWMutex
	loggers map[string]*zap.SugaredLogger
}

type ZapLogger struct {
	factory *zapFactory
	name    string
}

func NewZapLogger(cfg Config) (Logger, error) {
	if err := os.MkdirAll(cfg.Dir, 0o755); err != nil {
		return nil, fmt.Errorf("create log dir failed: %w", err)
	}
	if cfg.DefaultFile == "" {
		cfg.DefaultFile = "app.log"
	}
	if cfg.Files == nil {
		cfg.Files = map[string]string{}
	}
	f := &zapFactory{
		cfg:     cfg,
		loggers: map[string]*zap.SugaredLogger{},
	}
	return &ZapLogger{
		factory: f,
		name:    "app",
	}, nil
}

func (z *ZapLogger) Debugf(format string, args ...any) {
	z.get().Debugf(format, args...)
}

func (z *ZapLogger) Infof(format string, args ...any) {
	z.get().Infof(format, args...)
}

func (z *ZapLogger) Warnf(format string, args ...any) {
	z.get().Warnf(format, args...)
}

func (z *ZapLogger) Errorf(format string, args ...any) {
	z.get().Errorf(format, args...)
}

func (z *ZapLogger) Named(name string) Logger {
	if name == "" {
		return z
	}
	return &ZapLogger{
		factory: z.factory,
		name:    name,
	}
}

func (z *ZapLogger) Sync() error {
	return z.get().Sync()
}

func (z *ZapLogger) get() *zap.SugaredLogger {
	z.factory.mu.RLock()
	l, ok := z.factory.loggers[z.name]
	z.factory.mu.RUnlock()
	if ok {
		return l
	}

	z.factory.mu.Lock()
	defer z.factory.mu.Unlock()
	if l, ok = z.factory.loggers[z.name]; ok {
		return l
	}
	core := zapcore.NewCore(
		zapcore.NewJSONEncoder(zapcore.EncoderConfig{
			TimeKey:        "time",
			LevelKey:       "level",
			NameKey:        "logger",
			CallerKey:      "caller",
			MessageKey:     "msg",
			StacktraceKey:  "stacktrace",
			LineEnding:     zapcore.DefaultLineEnding,
			EncodeLevel:    zapcore.LowercaseLevelEncoder,
			EncodeTime:     zapcore.ISO8601TimeEncoder,
			EncodeDuration: zapcore.SecondsDurationEncoder,
			EncodeCaller:   zapcore.ShortCallerEncoder,
		}),
		zapcore.AddSync(&lumberjack.Logger{
			Filename:   filepath.Join(z.factory.cfg.Dir, z.fileName()),
			MaxSize:    z.factory.cfg.MaxSizeMB,
			MaxBackups: z.factory.cfg.MaxBackups,
			MaxAge:     z.factory.cfg.MaxAgeDays,
			Compress:   z.factory.cfg.Compress,
		}),
		zap.DebugLevel,
	)
	l = zap.New(core, zap.AddCaller(), zap.AddCallerSkip(1)).
		Named(z.name).
		Sugar()
	z.factory.loggers[z.name] = l
	return l
}

func (z *ZapLogger) fileName() string {
	if file, ok := z.factory.cfg.Files[z.name]; ok && file != "" {
		return file
	}
	if z.name == "app" {
		return z.factory.cfg.DefaultFile
	}
	return z.name + ".log"
}
