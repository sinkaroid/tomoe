import janda
import requests
import os
import re
import time
from .utils.misc import (
    choose,
    split_name,
    get_size,
    convert_html_to_pdf,
    project,
    get_size_folder,
    log_data,
    log_file,
    log_final,
)
from inputimeout import inputimeout, TimeoutOccurred

hfox = janda.Hentaifox()
t: str = "tomoe.html"


async def get_hfox(id: int = choose().hentaifox):
    initial = time.time()
    data = await hfox.get(id)
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

    if len(img) == len(os.listdir(neat_dir)):
        print(
            "All images already downloaded! If you're doubt kindly remove this folder and re-download"
        )
        print(f"Directory: {os.path.abspath(neat_dir)}")
        return

    for i in img:
        start = time.time()
        img_url = i

        try:
            r = requests.get(img_url)
            if r.status_code == 200:
                img_url = img_url
            else:
                img_url = re.sub(r"(?<=\d{3})\d{3}", r.status_code, img_url)
        except:
            img_url = img_url.replace(".jpg", ".png")

        img_name = img_url.rsplit("/", 1)[-1]

        r = requests.get(img_url)
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

                with open(neat_dir + "/" + t, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{parser['data']['id']}</h1>")

                    for i in img:
                        img_url = i
                        try:
                            r = requests.get(img_url)
                            if r.status_code == 200:
                                img_url = img_url
                            else:
                                img_url = re.sub(
                                    r"(?<=\d{3})\d{3}", r.status_code, img_url
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
                    desired = inputimeout(
                        prompt="Do you want to render it all to .pdf? (y/n) ",
                        timeout=10,
                    )
                    to_pdf = desired

                    if to_pdf == "y":
                        try:
                            source = open(f"{neat_dir}/{t}")
                            output = f"{neat_dir}/{parser['data']['id']}.pdf"
                            filepdf = output.rsplit("/", 1)[-1]

                            convert_html_to_pdf(source, output)
                            print(
                                f"Successfully rendered to {filepdf} | {get_size(output)} MB"
                            )

                        except Exception as e:
                            print(f"Something went wrong while converting to pdf: {e}")

                    elif to_pdf == "n":
                        print("Okay")
                        os.remove(neat_dir + "/" + t)
                        return

                    else:
                        print("Invalid input")
                        os.remove(neat_dir + "/" + t)
                        return

                except TimeoutOccurred:
                    print("Timeout occurred")
                    os.remove(neat_dir + "/" + t)
                    exit()
