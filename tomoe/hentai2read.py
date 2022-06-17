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

h2r = janda.Hentai2read()
t: str = "tomoe.html"

value = choose().hentai2read
if value is None:
    par1 = ""
    par2 = ""

else:
    value.sort()
    par1 = value[1]
    par2 = value[0]


async def get_h2r(id: str = par1, chapter: int = par2):
    initial = time.time()
    data = await h2r.get(id[0], chapter)
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

    if len(img) == len(os.listdir(neat_dir)):
        print(
            "All images already downloaded! If you're doubt kindly remove this folder and re-download"
        )
        print(f"Directory: {os.path.abspath(neat_dir)}")
        return

    for i in img:
        start = time.time()
        img_url = i
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
                print(f"Directory: {os.path.abspath(neat_dir)}")

                with open(neat_dir + "/" + t, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{parser['data']['title']}</h1>")

                    for i in img:
                        file = i.rsplit("/", 1)[-1]

                        f.write(f'<img src="{neat_dir}/{file}"><p></p>')
                    f.write(f"{project()}")
                    f.write("</body></center></html>")
                    f.close()

                try:
                    desired = inputimeout(
                        prompt="Do you want to render it all to .pdf? (y/n) ",
                        timeout=10,
                    )
                    to_pdf = desired

                    if to_pdf == "y":
                        try:
                            source = open(f"{neat_dir}/{t}")
                            output = f"{neat_dir}/{parser['data']['title']}.pdf"
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
