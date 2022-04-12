import json

from mitmproxy import ctx

logger = ctx.log


def request(flow):
    # flow是一个HTTPFlow对象
    # flow.request.headers["User-Agent"] = 'Tian'  # 修改请求头中的UA
    # flow.request.url = 'https://www.baidu.com'
    # ctx.log.info(str(flow.request.headers))
    # ctx.log.error(str(flow.request.host))
    logger.info(f'url;{flow.request.url}')


def response(flow):
    # res = flow.response
    # ctx.log.info(str(res.text))
    url = 'https://app5.scrape.center/api/movie'
    if flow.request.url.startswith(url):
        text = flow.response.text
        if not text:
            return
        data = json.loads(text)
        items = data.get('results')
        for item in items:
            logger.info(str(item))
