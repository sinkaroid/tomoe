import asyncio
from tomoe.tomoe.pururin import get_pur
from tomoe.tomoe.nhentai import get_nh
from tomoe.tomoe.simplyh import get_sim
from tomoe.tomoe.hentaifox import get_hfox
from tomoe.tomoe.hentai2read import get_h2r
from tomoe.tomoe.qhentai import get_qh
from tomoe.tomoe.asmhentai import get_asm
from tomoe.tomoe.utils.misc import choose, need_args

class Tomoe():
    def __init__(self,
                 Pururin: str = choose().pururin,
                 Nhentai: str = choose().nhentai,
                 Simplyhentai: str = choose().simply,
                 Haentaifox: str = choose().hentaifox,
                 Hentai2read: str = choose().hentai2read,
                 Qhentai: str = choose().qhentai,
                 Asmhentai: str = choose().asmhentai):

        self.pururin = Pururin
        self.nhentai = Nhentai
        self.simply = Simplyhentai
        self.hentaifox = Haentaifox
        self.hentai2read = Hentai2read
        self.qhentai = Qhentai
        self.asmhentai = Asmhentai


Api = Tomoe()


def main():
    async def main_pururin():
        await asyncio.gather(get_pur(Api.pururin))

    async def main_nhentai():
        await asyncio.gather(get_nh(Api.nhentai))

    async def main_simply():
        await asyncio.gather(get_sim(Api.simply))

    async def main_hentaifox():
        await asyncio.gather(get_hfox(Api.hentaifox))

    async def main_hentai2read():
        await asyncio.gather(get_h2r(Api.hentai2read))

    async def main_qhentai():
        await asyncio.gather(get_qh(Api.qhentai))

    async def main_asmhentai():
        await asyncio.gather(get_asm(Api.asmhentai))
   

    if Api.pururin is not None:
        asyncio.run(main_pururin())

    elif Api.nhentai is not None:
        asyncio.run(main_nhentai())

    elif Api.simply is not None:
        asyncio.run(main_simply())

    elif Api.hentaifox is not None:
        asyncio.run(main_hentaifox())

    elif Api.hentai2read is not None:
        asyncio.run(main_hentai2read())

    elif Api.qhentai is not None:
        asyncio.run(main_qhentai())

    elif Api.asmhentai is not None:
        asyncio.run(main_asmhentai())

    else:
        need_args()


if __name__ == '__main__':
    main()
