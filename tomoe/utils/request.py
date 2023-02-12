import aiohttp
from tomoe import __version__

header: dict = {
    "User-Agent": f"tomoe/v{__version__} (https://pypi.org/project/tomoe);",
    "From": "hey@sinkaroid.org",
},


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
