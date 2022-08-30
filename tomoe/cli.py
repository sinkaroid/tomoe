import asyncio
import sys
import os
from tomoe.tomoe.pururin import get_pur
from tomoe.tomoe.nhentai import get_nh
from tomoe.tomoe.simplyh import get_sim
from tomoe.tomoe.hentaifox import get_hfox
from tomoe.tomoe.hentai2read import get_h2r
from tomoe.tomoe.asmhentai import get_asm
from tomoe.tomoe.bulk_download import get_bulk
from tomoe.tomoe.utils.misc import choose, need_args


class Tomoe:
    def __init__(
        self,
        Pururin: str = choose().pururin,
        Nhentai: str = choose().nhentai,
        Simplyhentai: str = choose().simply,
        Haentaifox: str = choose().hentaifox,
        Hentai2read: str = choose().hentai2read,
        Asmhentai: str = choose().asmhentai,
        Bulk: str = choose().bulk,
    ):

        self.pururin = Pururin
        self.nhentai = Nhentai
        self.simply = Simplyhentai
        self.hentaifox = Haentaifox
        self.hentai2read = Hentai2read
        self.asmhentai = Asmhentai
        self.bulk = Bulk


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

    async def main_asmhentai():
        await asyncio.gather(get_asm(Api.asmhentai))

    async def main_bulk():
        await asyncio.gather(get_bulk(Api.bulk))

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

    elif Api.asmhentai is not None:
        asyncio.run(main_asmhentai())

    elif Api.bulk is not None:
        asyncio.run(main_bulk())

    else:
        need_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
