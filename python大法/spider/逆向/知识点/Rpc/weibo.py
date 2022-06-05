# @Time : 2022/6/5 21:46
# @Author :bo~
# @FileName: weibo.py
# @Description:
"""
https://weibo.com/login.php
浏览器override或fiddler替换也行

在相应的函数中启动websocket客户端
代码：
        !function() {
            if (window.flagLX) {} else {
                window.weiboLX = makeRequest;
                var ws = new WebSocket("ws://127.0.0.1:9999");
                window.flagLX = true;
                ws.open = function(evt) {}
                ;
                ws.onmessage = function(evt) {
                    var lx = evt.data;
                    var result = lx.split(',');
                    var res = window.weiboLX(result[0], result[1], 7, false);
                    ws.send(JSON.stringify(res));
                }
            }
        }();
Python创建一个websocket服务端
"""

import asyncio
import websockets


async def check_permit(websocket):
    for send_text in ['1111111,11111', '222222222,2222']:
        await websocket.send(send_text)
    return True


async def recv_msg(websocket):
    while 1:
        recv_text = await websocket.recv()
        print(recv_text)


async def main(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


asyncio.get_event_loop().run_until_complete(websockets.serve(main, 'localhost', 9999))
asyncio.get_event_loop().run_forever()
