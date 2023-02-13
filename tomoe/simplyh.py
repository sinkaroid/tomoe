import janda
import asyncio
import os
import re
import time
from .utils.request import get
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
    nums,
    project,
    split_name,
)

simply = janda.SimplyHentai()


async def get_sim(ids=choose().simply):
    for id in ids:
        await asyncio.gather(process_simplyh(id))
        print(f"Complete process {id}")


async def process_simplyh(id: str):
    initial = time.time()
    data = await simply.get(id)
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

    neat_dir = f"{split_name(__file__)}-{title}"
    neat_dir = re.sub("[^A-Za-z0-9-]+", " ", neat_dir)

    neat_dir = re.sub(r"\s+", "_", neat_dir)

    set_name = parser["data"]["id"]
    set_name = set_name.split("/")[-1]

    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(os.listdir(neat_dir)) - 1 == len(img):
        print(
            "All images already downloaded! If you're doubt kindly remove this folder and re-download"
        )
        print(f"Directory: {os.path.abspath(neat_dir)}")
        return

    for i in range(len(img)):
        start = time.time()

        while True:
            try:
                content_bytes = await get(img[i])
                break
            except Exception as e:
                log_warn(e, f"Retrying {img[i]} in 3 seconds...")
                time.sleep(3)
                continue

        with open(f"{neat_dir}/{i+1}.jpg", "wb") as f:
            f.write(content_bytes)

            if os.path.exists(f"{neat_dir}/{i+1}.jpg"):
                file = get_size(f"{neat_dir}/{i+1}.jpg")
                log_file(i + 1, file, f"{time.time() - start:.2f}")
                ## print(f"Successfully downloaded {i+1} | {file} MB | took {time.time() - start:.2f} seconds")

            if len(img) == len(os.listdir(neat_dir)):
                log_final(
                    f"{(time.time() - initial) / 60:.2f}", get_size_folder(neat_dir)
                )

                print(f"Directory: {os.path.abspath(neat_dir)}")

                with open(neat_dir + "/" + TOMOE_HTML, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{neat_dir}</h1>")

                    for i in nums(1, len(img)):

                        f.write(f'<img src="{neat_dir}/{i}.jpg"><p></p>')
                    f.write(f"{project()}")
                    f.write("</body></center></html>")
                    f.close()

                try:
                    process_pdf(neat_dir, set_name)
                except TimeoutOccurred:
                    print(f"Timeout occurred, not rendering pdf {id}")
