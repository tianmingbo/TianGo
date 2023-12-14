import asyncio


class Conn:
    # 异步上下文管理器
    async def __aenter__(self):
        print("create connect")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("release connect")


async def main():
    async with Conn() as conn:
        print('do somthing')


if __name__ == '__main__':
    asyncio.run(main())
