import aiohttp

async def get(url) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.content.read()
        
async def check_status(url) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status
