import janda
import json
import requests
import os
import re
import time
from .utils.misc import choose, split_name

nh = janda.Nhentai()


async def get_nh(id: int = choose().nhentai):
    data = await nh.get(id)
    parser = json.loads(data)

    title = parser['details']['title']['pretty']
    title = re.sub(r'[^\w\s]', '', title)
    print(f'Title: {title}')

    img = parser['image_urls']
    print(f'Total image: {len(img)}')

    neat_dir = split_name(__file__) + " - " + title

    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(os.listdir(neat_dir)) - 1 == len(img):
        print("All images already downloaded! If you're doubt kindly remove this folder and re-download")
        print(f'Directory: {os.path.abspath(neat_dir)}')
        return

    for i in img:
        start = time.time()
        img_url = i
        img_name = img_url.rsplit('/', 1)[-1]

        r = requests.get(img_url)
        with open(neat_dir + '/' + img_name, 'wb') as f:
            f.write(r.content)

            if os.path.exists(neat_dir + '/' + img_name):
                print(
                    f'Successfully downloaded {img_name} | in {time.time() - start:.2f} seconds')

            if len(img) == len(os.listdir(neat_dir)):
                print("All images downloaded!")
                with open(neat_dir + '/gallery.html', 'w') as f:
                    f.write('<html><body>')
                    for i in os.listdir(neat_dir):
                        f.write(f'<img src="{i}">')
                    f.write('</body></html>')

                    print(f'Static gallery saved to {neat_dir}/gallery.html')
                    print(f'Directory: {os.path.abspath(neat_dir)}')
