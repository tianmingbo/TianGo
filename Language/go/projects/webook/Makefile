.PHONY: docker
docker:
	# 把上次编译的东西删掉
	@rm webook || true
	@docker rmi -f webook:v0.0.1
	# 指定编译成在 ARM 架构的 linux 操作系统上运行的可执行文件，
	# 名字叫做 webook
	@GOOS=linux GOARCH=arm go build -tags=k8s -o webook .
	# 这里你可以随便改这个标签，记得对应的 k8s 部署里面也要改
	@docker build -t webook:v0.0.1 .
mock:
	@mockgen -source=internal/service/code.go -package=svcmocks -destination=internal/service/mocks/code.mock.go
	@mockgen -source=internal/service/user.go -package=svcmocks -destination=internal/service/mocks/user.mock.go
	@mockgen -source=internal/repository/user.go -package=repomocks -destination=internal/repository/mocks/user.mock.go
	@mockgen -source=internal/repository/code.go -package=repomocks -destination=internal/repository/mocks/code.mock.go
	@mockgen -source=internal/repository/dao/user.go -package=daomocks -destination=internal/repository/dao/mocks/user.mock.go
	@mockgen -source=internal/repository/cache/user.go -package=cachemocks -destination=internal/repository/cache/mocks/user.mock.go
	@mockgen -package=redismocks -destination=internal/repository/cache/redismocks/cmdable.mock.go github.com/redis/go-redis/v9 Cmdable
	@go mod tidy