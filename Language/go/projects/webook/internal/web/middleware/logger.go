package middleware

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
	"webook/pkg/logger"

	"github.com/gin-gonic/gin"
)

type AccessLogMiddlewareBuilder struct {
	l            logger.Logger
	maxBodyBytes int
}

func NewAccessLogMiddlewareBuilder(l logger.Logger) *AccessLogMiddlewareBuilder {
	return &AccessLogMiddlewareBuilder{
		l:            l,
		maxBodyBytes: 2048,
	}
}

func (b *AccessLogMiddlewareBuilder) MaxBodyBytes(n int) *AccessLogMiddlewareBuilder {
	if n > 0 {
		b.maxBodyBytes = n
	}
	return b
}

func (b *AccessLogMiddlewareBuilder) Build() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		start := time.Now()
		reqBody := readAndRestoreRequestBody(ctx.Request, b.maxBodyBytes)

		blw := &bodyLogWriter{
			ResponseWriter: ctx.Writer,
			body:           bytes.NewBuffer(nil),
		}
		ctx.Writer = blw
		ctx.Next()

		cost := time.Since(start)
		respBody := truncate(blw.body.String(), b.maxBodyBytes)
		line := fmt.Sprintf("method=%s path=%s query=%q status=%d cost=%s ip=%s req=%q resp=%q",
			ctx.Request.Method, ctx.FullPath(), ctx.Request.URL.RawQuery, ctx.Writer.Status(),
			cost, ctx.ClientIP(), reqBody, respBody)
		if len(ctx.Errors) > 0 || ctx.Writer.Status() >= http.StatusInternalServerError {
			b.l.Errorf(line)
			return
		}
		b.l.Infof(line)
	}
}

type bodyLogWriter struct {
	gin.ResponseWriter
	body *bytes.Buffer
}

func (w *bodyLogWriter) Write(data []byte) (int, error) {
	w.body.Write(data)
	return w.ResponseWriter.Write(data)
}

func (w *bodyLogWriter) WriteString(s string) (int, error) {
	w.body.WriteString(s)
	return w.ResponseWriter.WriteString(s)
}

func readAndRestoreRequestBody(req *http.Request, maxBytes int) string {
	if req == nil || req.Body == nil {
		return ""
	}
	raw, err := io.ReadAll(req.Body)
	if err != nil {
		return fmt.Sprintf("read_request_body_failed:%v", err)
	}
	req.Body = io.NopCloser(bytes.NewReader(raw))
	return truncate(string(raw), maxBytes)
}

func truncate(s string, maxBytes int) string {
	if maxBytes <= 0 || len(s) <= maxBytes {
		return strings.TrimSpace(s)
	}
	return strings.TrimSpace(s[:maxBytes]) + "...(truncated)"
}
