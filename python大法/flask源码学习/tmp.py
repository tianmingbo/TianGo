import asyncio
import contextvars

# 定义一个上下文变量
request_id = contextvars.ContextVar("request_id")


async def process_request(user_id):
    # 在协程中设置上下文变量的值
    request_id.set(user_id)
    await asyncio.sleep(1)
    await process_data()


async def process_data():
    # 在协程中访问上下文变量的值
    print("Processing request with id:", request_id.get())


async def main():
    # 启动多个协程来处理请求
    await asyncio.gather(
        process_request(123),
        process_request(456)
    )


if __name__ == "__main__":
    asyncio.run(main())
