import janda
import json
import requests
import os
import re
import time
from .utils.misc import choose, split_name, get_size, convert_html_to_pdf, project
from inputimeout import inputimeout, TimeoutOccurred

nh = janda.Nhentai()


async def get_nh(id: int = choose().nhentai):
    initial = time.time()
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

    if len(os.listdir(neat_dir)) >= len(img):
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
                    f'Successfully downloaded {img_name} | {get_size(neat_dir + "/" + img_name)} MB | in {time.time() - start:.2f} seconds')

            if len(img) == len(os.listdir(neat_dir)):
                print(
                    f'Successfully downloaded all images in {(time.time() - initial) / 60:.2f} minutes')
                with open(neat_dir + '/deleteme.phtml', 'x') as f:
                    f.write('<html><center><body>')
                    f.write(f'<h1>{title}</h1>')
                    ## print(os.listdir(neat_dir)[:-1])
                    for i in os.listdir(neat_dir)[:-1]:
                        ## write all images with valid name and path
                        f.write(f'<img src="{neat_dir}/{i}"><p></p>')
                    f.write(f'{project()}')
                    f.write('</body></center></html>')

                    print(f'Static gallery saved to {neat_dir}/deleteme.phtml')
                    print(f'Directory: {os.path.abspath(neat_dir)}')

        
                try:
                    desired = inputimeout(prompt='Do you want to render it all to .pdf? (y/n) ', timeout=10)
                    to_pdf = desired

                    if to_pdf == 'y':
                        try:
                            source = open(f"{neat_dir}/deleteme.phtml")
                            output = f"{neat_dir}/{parser['details']['id']}.pdf"

                            convert_html_to_pdf(source, output)
                            print(f'Successfully converted to {output}')    

                        except Exception as e:
                            print(
                                f"Something went wrong while converting to pdf: {e}")
                                
                    elif to_pdf == 'n':
                        print("Okay")
                        os.remove(neat_dir + '/deleteme.phtml')
                        return

                    else:
                        print("Invalid input")
                        os.remove(neat_dir + '/deleteme.phtml')
                        return

                except TimeoutOccurred:
                    print("Timeout occurred")
                    exit()

