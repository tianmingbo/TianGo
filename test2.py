from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# 创建 FastAPI 实例
app = FastAPI()


# 定义根路由的 GET 请求处理器
@app.get("/")
async def read_root():
    return {"Hello": "World"}


class Item(BaseModel):
    name: str


# 处理 POST 请求
@app.post("/items/")
async def create_item(item: Item):
    # 在这里可以对接收到的请求体数据进行处理
    # 例如将数据存入数据库或进行其他操作
    return {"message": f"Item {item.name}"}


# 定义 /items/{item_id} 路由的 GET 请求处理器
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


if __name__ == '__main__':
    uvicorn.run(app)
