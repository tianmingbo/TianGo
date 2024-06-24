import datetime
import orjson
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.engine.url import URL
from sqlalchemy import text, Table, Column, MetaData
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

routes = web.RouteTableDef()


async def create_database_engine(app: web.Application):
    # 创建数据库池（在 sqlalchemy 中称为引擎），并将其存储在应用程序实例中。
    engine = create_async_engine(
        URL.create("mysql+asyncmy", username="root", password="123456",
                   host="127.0.0.1", port=3306, database="test")
    )
    app["engine"] = engine


async def destroy_database_engine(app: web.Application):
    engine: AsyncEngine = app["engine"]
    # 关闭引擎以及连接池，并清理所有的连接
    await engine.dispose()


@routes.get("/girl")
async def get_girls(request: Request) -> Response:
    # 获取引擎
    engine: AsyncEngine = request.app["engine"]
    # 构建查询 SQL
    query = text("SELECT name, age, address FROM girl")
    # 从池子里面拿出一个连接，执行查询
    async with engine.connect() as conn:
        rows = await conn.execute(query)
    # 拼接成字典
    keys = rows.keys()
    results = [dict(zip(keys, row)) for row in rows]
    return Response(body=orjson.dumps(results), content_type="application/json")


@routes.post("/girl")
async def post_girls(request: Request) -> Response:
    table = Table("girl", MetaData(),
                  Column("id", INTEGER, primary_key=True, autoincrement=True),
                  Column("name", VARCHAR(255)),
                  Column("age", INTEGER),
                  Column("address", VARCHAR(255)))
    engine: AsyncEngine = request.app["engine"]
    # 获取请求体，必须是一个 JSON
    content = await request.content.read()
    try:
        data = orjson.loads(content)
    except orjson.JSONDecodeError:
        return Response(body=orjson.dumps({"error": "请求体必须是一个 JSON"}),
                        content_type="application/json")
    # 需要对 data 里面的字段做一个检测，这里就不检测了
    query = table.insert().values(data)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()

    return Response(body=orjson.dumps({"message": "数据添加成功"}),
                    content_type="application/json")


@routes.get("/")
async def res(request: Request) -> Response:
    result = {
        "request.scheme（使用的协议）": request.scheme,
        "request.secure（协议是否是 https）": request.secure,
        "request.method（请求方法）": request.method,
        "request.version（HTTP 协议版本）": str(request.version),
        "request.host（客户端请求的主机名）": request.host,
        "request.remote（发起请求的客户端的 IP 地址）": request.remote,
        "request.url（客户端请求的 URL）": str(request.url),
        "request.path（客户端请求的路径，不带查询参数）": request.path,
        "request.path_qs（客户端请求的路径，带查询参数）": request.path_qs,
        "request.query（查询参数，像字典一样操作即可）": str(request.query),
        "request.query（查询参数，一个字符串）": request.query_string,
        "request.headers（请求头，像字典一样操作即可）": str(request.headers.__class__),
        "request.keep_alive（是否开启了长连接）": request.keep_alive,
        "request.cookies（cookie 信息，像字典一样操作即可）": str(request.cookies.__class__),
        "request.content（原始的字节流信息，针对 POST 和 PUT）": (await request.content.read()).decode("utf-8"),

    }
    return Response(body=orjson.dumps(result), content_type="application/json")


@routes.get("/share")
async def get_data(request: Request) -> Response:
    shared_data = request.app["shared_dict"]
    return Response(body=orjson.dumps(shared_data), content_type="application/json")


app = web.Application()
app["shared_dict"] = {"key": "value"}
# 应用程序（app）启动时会调用 create_database_engine 执行，以 app 为参数
# 在里面我们创建引擎，并保存在 app 中
app.on_startup.append(create_database_engine)
# 应用程序关闭时会调用 destroy_database_engine，在里面我们释放引擎
app.on_cleanup.append(destroy_database_engine)
app.add_routes(routes)
web.run_app(app, port=9999)
