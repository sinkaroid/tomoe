import janda
import json
import requests
import os
import re
import time
from .utils.misc import choose, split_name, get_size

simply = janda.SimplyHentai()


async def get_sim(id: str = choose().simply):
    initial = time.time()
    data = await simply.get(id)
    parser = json.loads(data)

    title = parser['title']
    title = re.sub(r'[^\w\s]', '', title)
    print(f'Title: {title}')

    img = parser['image']
    print(f'Total image: {len(img)}')

    neat_dir = split_name(__file__) + " - " + title

    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(os.listdir(neat_dir)) - 1 == len(img):
        print("All images already downloaded! If you're doubt kindly remove this folder and re-download")
        print(f'Directory: {os.path.abspath(neat_dir)}')
        return

    for i in range(len(img)):
        start = time.time()
        r = requests.get(img[i])
        with open(f"{neat_dir}/{i+1}.jpg", 'wb') as f:
            f.write(r.content)

            if os.path.exists(f"{neat_dir}/{i+1}.jpg"):
                file = get_size(f"{neat_dir}/{i+1}.jpg")
                print(
                    f'Successfully downloaded {i+1} | {file} MB | in {time.time() - start:.2f} seconds')

            if len(img) == len(os.listdir(neat_dir)):
                ## print time elapsed as minutes not second
                print(f'Successfully downloaded all images in {(time.time() - initial) / 60:.2f} minutes')
                with open(neat_dir + '/gallery.html', 'w') as f:
                    f.write('<html><body>')
                    for i in os.listdir(neat_dir):
                        f.write(f'<img src="{i}">')
                    f.write('</body></html>')

                    print(f'Static gallery saved to {neat_dir}/gallery.html')
                    print(f'Directory: {os.path.abspath(neat_dir)}')
