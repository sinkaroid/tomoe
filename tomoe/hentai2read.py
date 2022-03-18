import janda
import json
import requests
import os
import re
import time
from .utils.misc import choose, split_name

h2r = janda.Hentai2read() 


async def get_h2r(id: str = choose().hentai2read):
    data = await h2r.get(id)
    parser = json.loads(data)
    title = parser['title']
    title = re.sub(r'[^\w\s]','', title)
    print(f'Title: {title}')

    img = parser['images']
    print(f'Total image: {len(img)}')
    neat_dir = split_name(__file__) + " - " + title
    
    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(img) == len(os.listdir(neat_dir)):
        print("All images already downloaded! If you're doubt kindly remove this folder and re-download")
        print(f'Directory: {os.path.abspath(neat_dir)}')
        return

    for i in img:
        start = time.time()
        img_url = i
        img_name = img_url.rsplit('/', 1)[-1]

        r = requests.get(f'https://static.hentaicdn.com/hentai{img_url}')
        with open(neat_dir + '/' + img_name, 'wb') as f:
            f.write(r.content)
     
            if os.path.exists(neat_dir + '/' + img_name):
                print(f'Successfully downloaded {img_name} | in {time.time() - start:.2f} seconds')
            
            if len(img) == len(os.listdir(neat_dir)):
                print("All images downloaded!")
                with open(neat_dir + '/gallery.html', 'w') as f:
                    f.write('<html><body>')
                    for i in os.listdir(neat_dir):
                        f.write(f'<img src="{i}">')
                    f.write('</body></html>')

                    print(f'Static gallery saved to {neat_dir}/gallery.html')
                    print(f'Directory: {os.path.abspath(neat_dir)}')
