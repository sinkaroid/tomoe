import asyncio
import json
import time
from .utils.misc import choose
from .pururin import process_pururin
from .nhentai import process_nhentai
from .hentaifox import process_hentaifox
from .asmhentai import process_asmhentai
from .hentai2read import process_h2r
from .simplyh import process_simplyh


async def get_bulk(book: str = choose().bulk):
    f = open(book)

    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        print(
            "Invalid bulk file, does not follow the nested JSON format.\nGuide: https://github.com/sinkaroid/tomoe#bulk-download-using-nested-list"
        )
        return

    initial = time.time()
    print(f'Requesting {len(data["book"])} doujinshi..')

    for i in data["book"]:
        for key, value in i.items():
            ## print(key, value)
            if key.startswith("pur"):
                await asyncio.gather(process_pururin(value))
            elif key.startswith("nh"):
                await asyncio.gather(process_nhentai(value))
            elif key.startswith("hentaif"):
                await asyncio.gather(process_hentaifox(value))
            elif key.startswith("asm"):
                await asyncio.gather(process_asmhentai(value))
            elif key.startswith("simply"):
                await asyncio.gather(process_simplyh(value))
            elif key.startswith("hentai2"):
                h2r_path = value.split(":")
                await asyncio.gather(process_h2r(value))

            else:
                print("An unexpected property that does not support:", key, value)
                pass

    print(
        f"Bulk download completed, took: {(time.time() - initial) / 60:.2f}"
        + " minutes"
    )
    f.close()
