import asyncio
import os
import re
import time

import janda
import requests
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

h2r = janda.Hentai2read()


async def get_h2r(ids=choose().hentai2read):
    for id in ids:
        par = id.split(":")
        await asyncio.gather(process_h2r(par[0], par[1]))
        print(f"Complete process {par[0]}, chapter {par[1]}")


async def process_h2r(id: str, chapter: int):
    initial = time.time()
    data = await h2r.get(id, chapter)
    parser = janda.resolve(data)

    title = re.sub(r"[^\w\s]", "", parser["data"]["title"])
    img = parser["data"]["image"]
    slug = parser["data"]["id"]

    log_data("TITLE", title)
    log_data("ID", slug)
    log_data("SOURCE", parser["current_url"])
    log_data("TOTAL", f"{len(parser['data']['image'])} pages")

    neat_dir = split_name(__file__) + " - " + title
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
        img_name = img_url.rsplit("/", 1)[-1]

        while True:
            try:
                r = requests.get(img_url)
                break
            except Exception as e:
                log_warn(e, f"Retrying {img_name} in 3 seconds...")
                time.sleep(3)
                continue

        with open(neat_dir + "/" + img_name, "wb") as f:

            f.write(r.content)

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
                print(f"Directory: {os.path.abspath(neat_dir)}")

                with open(neat_dir + "/" + TOMOE_HTML, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{parser['data']['title']}</h1>")

                    for i in img:
                        file = i.rsplit("/", 1)[-1]

                        f.write(f'<img src="{neat_dir}/{file}"><p></p>')
                    f.write(f"{project()}")
                    f.write("</body></center></html>")
                    f.close()

                try:
                    process_pdf(neat_dir, parser["data"]["title"])
                except TimeoutOccurred:
                    print(
                        f"Timeout occurred, not rendering pdf {id}, chapter: {chapter}"
                    )
