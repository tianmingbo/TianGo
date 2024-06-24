import uvicorn


async def application(scope, receive, send):
    await send(
        {"type": "http.response.start",
         "status": 200,
         "headers": [(b"Content-Type", b"text/html")]}
    )
    await send({"type": "http.response.body", "body": b"ASGI hello!"})


if __name__ == '__main__':
    uvicorn.run(application)
