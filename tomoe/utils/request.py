import aiohttp

async def get(url) -> bytes:
    """Get content bytes from url.
    
    Parameters
    ----------
    url : str
        URL to get content from

    Returns
    -------
    bytes
        The content bytes from url
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.content.read()
        
async def check_status(url) -> int:
    """Check status code from url.

    Parameters
    ----------
    url : str
        URL to check status code from

    Returns
    -------
    int
        The status code from url
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status
