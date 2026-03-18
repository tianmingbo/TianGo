package logger

import (
	"log"
	"os"
)

type StdLogger struct {
	debug *log.Logger
	info  *log.Logger
	warn  *log.Logger
	error *log.Logger
}

func NewStdLogger() Logger {
	return &StdLogger{
		debug: log.New(os.Stdout, "[DEBUG] ", log.LstdFlags|log.Lmicroseconds|log.Lshortfile),
		info:  log.New(os.Stdout, "[INFO] ", log.LstdFlags|log.Lmicroseconds|log.Lshortfile),
		warn:  log.New(os.Stdout, "[WARN] ", log.LstdFlags|log.Lmicroseconds|log.Lshortfile),
		error: log.New(os.Stderr, "[ERROR] ", log.LstdFlags|log.Lmicroseconds|log.Lshortfile),
	}
}

func (s *StdLogger) Debugf(format string, args ...any) {
	s.debug.Printf(format, args...)
}

func (s *StdLogger) Infof(format string, args ...any) {
	s.info.Printf(format, args...)
}

func (s *StdLogger) Warnf(format string, args ...any) {
	s.warn.Printf(format, args...)
}

func (s *StdLogger) Errorf(format string, args ...any) {
	s.error.Printf(format, args...)
}

func (s *StdLogger) Named(name string) Logger {
	return s
}

func (s *StdLogger) Sync() error {
	return nil
}
