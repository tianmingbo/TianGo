# python为了将语义变得更加明确，就引入了async和await关键词用于定义原生的协程
# async def downloader(url):
#     return "dali"
import types


@types.coroutine
def downloader(url):
    yield "dali"


async def download_url(url):
    # dosomethings
    html = await downloader(url)
    print("html")
    return html


if __name__ == "__main__":
    coro = download_url("http://www.imooc.com")
    # next(None)
    coro.send(None)
