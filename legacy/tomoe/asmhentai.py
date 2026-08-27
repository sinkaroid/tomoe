import janda
import asyncio
import os
import re
import time
from .utils.request import get, check_status
from inputimeout import TimeoutOccurred

from .pdf import process_pdf
from .utils.const import TOMOE_HTML
from .utils.misc import (
    choose,
    get_size,
    get_size_folder,
    log_data,
    log_file,
    log_final,
    log_warn,
    project,
    split_name,
)

asmh = janda.Asmhentai()


async def get_asm(ids=choose().asmhentai):
    for id in ids:
        await asyncio.gather(process_asmhentai(id))
        print(f"Complete process {id}")


async def process_asmhentai(id: int):
    initial = time.time()
    data = await asmh.get(id)
    parser = janda.resolve(data)

    title = re.sub(r"[^\w\s]", "", parser["data"]["title"])
    img = parser["data"]["image"]
    number = parser["data"]["id"]
    tags = parser["data"]["tags"]
    tags = [tag for tag in tags]
    to_tags = ", ".join(tags)

    log_data("TITLE", title)
    log_data("TAGS", to_tags)
    log_data("ID", number)
    log_data("SOURCE", parser["source"])
    log_data("TOTAL", f"{parser['data']['total']} pages")

    neat_dir = f"{split_name(__file__)}-{number}-{title}"
    neat_dir = re.sub("[^A-Za-z0-9-]+", " ", neat_dir)

    neat_dir = re.sub(r"\s+", "_", neat_dir)

    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(img) == len(os.listdir(neat_dir)) or len(img) <= len(os.listdir(neat_dir)):
        print(
            "All images already downloaded! If you're doubt kindly remove this folder and re-download"
        )
        print(f"Directory: {os.path.abspath(neat_dir)}")
        return

    for i in img:
        start = time.time()
        img_url = i

        try:
            while True:
                try:
                    r = await check_status(img_url)
                    break
                except Exception as e:
                    log_warn(e, f"Retrying {img_url} in 3 seconds...")
                    time.sleep(3)
                    continue

            if r == 200:
                img_url = img_url
            else:
                img_url = re.sub(r"(?<=\d{3})\d{3}", r, img_url)
        except:
            img_url = img_url.replace(".jpg", ".png")

        img_name = img_url.rsplit("/", 1)[-1]

        r = await get(img_url)
        with open(neat_dir + "/" + img_name, "wb") as f:

            f.write(r)

            if os.path.exists(neat_dir + "/" + img_name):
                log_file(
                    img_name,
                    get_size(neat_dir + "/" + img_name),
                    f"{time.time() - start:.2f}",
                )

            if len(img) == len(os.listdir(neat_dir)):
                log_final(
                    f"{(time.time() - initial) / 60:.2f}", get_size_folder(neat_dir)
                )

                with open(neat_dir + "/" + TOMOE_HTML, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{parser['data']['id']}</h1>")

                    for i in img:
                        img_url = i
                        try:
                            r = await check_status(img_url)
                            if r == 200:
                                img_url = img_url
                            else:
                                img_url = re.sub(
                                    r"(?<=\d{3})\d{3}", r, img_url
                                )
                        except:
                            img_url = img_url.replace(".jpg", ".png")

                        file = img_url.rsplit("/", 1)[-1]

                        f.write(f'<img src="{neat_dir}/{file}"><p></p>')
                    f.write(f"{project()}")
                    f.write("</body></center></html>")
                    f.close()

                    print(f"Directory: {os.path.abspath(neat_dir)}")

                try:
                    process_pdf(neat_dir, parser["data"]["id"])
                except TimeoutOccurred:
                    print(f"Timeout occurred, not rendering pdf {id}")
