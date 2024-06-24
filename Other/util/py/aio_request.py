import aiohttp
from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str, timeout=5):
    timeout = aiohttp.ClientTimeout(timeout)
    async with session.get(url, timeout=timeout) as response:
        return response.status
