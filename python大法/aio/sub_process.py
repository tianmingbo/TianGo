# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: sub_process.py
@time: 2024/1/6  20:49
@desc: 基于异步IO的子进程交互API
"""
import asyncio


async def main():
    # 把输出重定向到进程管道
    p = await asyncio.create_subprocess_shell('ls -al', stdout=asyncio.subprocess.PIPE)
    # 在没有结束之前一直读取数据，eof全称为END_OF_FILE，意为文件结尾，指该数据的结尾
    while not p.stdout.at_eof():
        line = await p.stdout.readline()
        if line:
            print(line)
    # await p.wait()


if __name__ == '__main__':
    asyncio.run(main())
