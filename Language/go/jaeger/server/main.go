package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"time"

	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
)

// initTracer 初始化Jaeger追踪器
func initTracer(serviceName string) (opentracing.Tracer, io.Closer) {
	cfg := config.Configuration{
		ServiceName: serviceName,
		Sampler: &config.SamplerConfig{
			Type:  jaeger.SamplerTypeConst,
			Param: 1, // 采样率100%
		},
		Reporter: &config.ReporterConfig{
			LocalAgentHostPort: "10.6.64.191:6831", // Jaeger Agent地址
			LogSpans:           true,
		},
	}

	tracer, closer, err := cfg.NewTracer(config.Logger(jaeger.StdLogger))
	if err != nil {
		log.Fatalf("无法初始化追踪器: %v", err)
	}

	// 设置全局追踪器
	opentracing.SetGlobalTracer(tracer)
	return tracer, closer
}

// serviceA 服务A：链路起点，调用服务B
func serviceA(ctx context.Context) {
	// 从上下文中获取父span或创建根span
	span, ctx := opentracing.StartSpanFromContext(ctx, "serviceA")
	defer span.Finish()

	// 设置标签
	ext.Component.Set(span, "serviceA")
	ext.HTTPMethod.Set(span, "GET")
	ext.HTTPUrl.Set(span, "/api/request")

	// 记录日志
	span.LogKV("event", "开始处理请求", "time", time.Now().Format(time.RFC3339))

	// 模拟处理时间
	time.Sleep(100 * time.Millisecond)

	// 调用服务B
	serviceB(ctx)

	// 记录完成日志
	span.LogKV("event", "请求处理完成")
	ext.HTTPStatusCode.Set(span, 200)
}

// serviceB 服务B：被服务A调用，调用服务C
func serviceB(ctx context.Context) {
	// 创建子span
	span, ctx := opentracing.StartSpanFromContext(ctx, "serviceB")
	defer span.Finish()

	span.SetTag("component", "serviceB")
	span.LogKV("event", "开始处理服务B逻辑")

	// 模拟处理时间
	time.Sleep(200 * time.Millisecond)

	// 调用服务C
	serviceC(ctx)

	span.LogKV("event", "服务B处理完成")
}

// serviceC 服务C：被服务B调用，包含数据库操作
func serviceC(ctx context.Context) {
	span, ctx := opentracing.StartSpanFromContext(ctx, "serviceC")
	defer span.Finish()

	span.SetTag("component", "serviceC")
	span.LogKV("event", "开始处理服务C逻辑")

	// 模拟数据库查询
	dbQuery(ctx)

	// 模拟处理时间
	time.Sleep(150 * time.Millisecond)

	span.LogKV("event", "服务C处理完成")
}

// dbQuery 模拟数据库查询操作
func dbQuery(ctx context.Context) {
	span, _ := opentracing.StartSpanFromContext(ctx, "dbQuery")
	defer span.Finish()

	ext.DBInstance.Set(span, "user_db")
	ext.DBStatement.Set(span, "SELECT * FROM users WHERE id = 1")
	span.LogKV("event", "开始数据库查询")

	// 模拟数据库查询耗时
	time.Sleep(120 * time.Millisecond)

	span.LogKV("event", "数据库查询完成", "result_count", 1)
}

func main() {
	// 初始化追踪器
	_, closer := initTracer("example-service")
	defer closer.Close()

	// 开始追踪
	ctx := context.Background()
	serviceA(ctx)

	// 等待追踪数据上报
	time.Sleep(2 * time.Second)
	fmt.Println("追踪完成，可在Jaeger UI查看结果")
}
