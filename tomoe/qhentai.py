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
)
from inputimeout import inputimeout, TimeoutOccurred

qhentai = janda.Qhentai()


async def get_qh(id: int = choose().qhentai):
    initial = time.time()
    data = await qhentai.get(id)
    parser = janda.resolve(data)
    title = parser["title"]
    title = re.sub(r"[^\w\s]", "", title)
    print(f"Title: {title}")

    img = parser["image"]
    number = parser["id"]
    print(f"Total: {len(img)}")
    print(f'Tags: {parser["tags"]}')
    neat_dir = f"{split_name(__file__)}-{title}"
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
        img_name = img_url.rsplit("/", 1)[-1]

        r = requests.get(img_url)
        with open(neat_dir + "/" + img_name, "wb") as f:

            f.write(r.content)

            if os.path.exists(neat_dir + "/" + img_name):
                print(
                    f'Successfully downloaded {img_name} | {get_size(neat_dir + "/" + img_name)} MB | took {time.time() - start:.2f} seconds'
                )

            if len(img) == len(os.listdir(neat_dir)):
                print(
                    f"Successfully downloaded all images taken {(time.time() - initial) / 60:.2f} minutes with total size {get_size_folder(neat_dir)} MB"
                )
                print(f"Directory: {os.path.abspath(neat_dir)}")

                with open(neat_dir + "/tomoe.html", "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{parser['id']}</h1>")

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
                            source = open(f"{neat_dir}/tomoe.html")
                            output = f"{neat_dir}/{parser['id']}.pdf"
                            filepdf = output.rsplit("/", 1)[-1]

                            convert_html_to_pdf(source, output)
                            print(
                                f"Successfully rendered to {filepdf} | {get_size(output)} MB"
                            )

                        except Exception as e:
                            print(f"Something went wrong while converting to pdf: {e}")

                    elif to_pdf == "n":
                        print("Okay")
                        os.remove(neat_dir + "/tomoe.html")
                        return

                    else:
                        print("Invalid input")
                        os.remove(neat_dir + "/tomoe.html")
                        return

                except TimeoutOccurred:
                    print("Timeout occurred")
                    os.remove(neat_dir + "/tomoe.html")
                    exit()
