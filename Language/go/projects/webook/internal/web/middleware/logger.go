package middleware

import (
	"bytes"
	"io"
	"net/http"
	"time"
	"webook/pkg/logger"

	"github.com/gin-gonic/gin"
)

const maxLoggedBodySize = 4 * 1024

type bodyLogWriter struct {
	gin.ResponseWriter
	body *bytes.Buffer
}

func (w *bodyLogWriter) Write(b []byte) (int, error) {
	if w.body.Len() < maxLoggedBodySize {
		remain := maxLoggedBodySize - w.body.Len()
		if len(b) > remain {
			w.body.Write(b[:remain])
		} else {
			w.body.Write(b)
		}
	}
	return w.ResponseWriter.Write(b)
}

// GinLoggerMiddleware 记录请求与响应关键信息（方法、路径、状态码、耗时、请求体、响应体）。
func GinLoggerMiddleware(logger logger.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		if logger == nil {
			c.Next()
			return
		}

		start := time.Now()
		method := c.Request.Method
		path := c.Request.URL.Path
		query := c.Request.URL.RawQuery
		clientIP := c.ClientIP()

		var reqBodyText string
		if c.Request.Body != nil {
			bodyBytes, err := io.ReadAll(c.Request.Body)
			if err == nil {
				c.Request.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
				reqBodyText = truncateText(string(bodyBytes), maxLoggedBodySize)
			} else {
				reqBodyText = "<read request body failed>"
			}
		}

		blw := &bodyLogWriter{
			ResponseWriter: c.Writer,
			body:           bytes.NewBuffer(nil),
		}
		c.Writer = blw

		c.Next()

		latency := time.Since(start)
		statusCode := c.Writer.Status()
		respBodyText := truncateText(blw.body.String(), maxLoggedBodySize)
		errText := c.Errors.ByType(gin.ErrorTypePrivate).String()

		levelLog := logger.Info
		if statusCode >= http.StatusInternalServerError {
			levelLog = logger.Error
		} else if statusCode >= http.StatusBadRequest {
			levelLog = logger.Warn
		}

		levelLog("http access",
			"method", method,
			"path", path,
			"query", query,
			"client_ip", clientIP,
			"status", statusCode,
			"latency_ms", latency.Milliseconds(),
			"request_body", reqBodyText,
			"response_body", respBodyText,
			"errors", errText,
		)
	}
}

func truncateText(in string, max int) string {
	if max <= 0 || len(in) <= max {
		return in
	}
	return in[:max] + "...(truncated)"
}
