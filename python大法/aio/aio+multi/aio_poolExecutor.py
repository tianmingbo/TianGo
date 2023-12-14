import asyncio
from concurrent.futures import ProcessPoolExecutor
from asyncio import AbstractEventLoop


def count(to: int) -> int:
    counter = 0
    while counter < to:
        counter += 1
    return counter


async def main():
    with ProcessPoolExecutor() as pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        numbers = [1, 3, 5, 22, 100000000]
        tasks = [loop.run_in_executor(pool, count, n) for n in numbers]
        res = await asyncio.gather(*tasks)

        print(res)


if __name__ == '__main__':
    asyncio.run(main())
