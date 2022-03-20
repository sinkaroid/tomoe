import janda
import json
import requests
import os
import re
import time
from .utils.misc import choose, split_name, get_size, convert_html_to_pdf, project, get_size_folder, nums
from inputimeout import inputimeout, TimeoutOccurred

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

    tags = parser['tags']
    tags = [tag for tag in tags]
    print(f'Tags: {tags}')

    neat_dir = f'{split_name(__file__)}-{title}'
    neat_dir = re.sub('[^A-Za-z0-9-]+', ' ', neat_dir)
  
    neat_dir = re.sub(r'\s+', '_', neat_dir)

    set_name = parser['id']
    set_name = set_name.split('/')[-1]

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
                    f'Successfully downloaded {i+1} | {file} MB | took {time.time() - start:.2f} seconds')

            if len(img) == len(os.listdir(neat_dir)):

                print(f'Successfully downloaded all images taken {(time.time() - initial) / 60:.2f} minutes with total size {get_size_folder(neat_dir)} MB')
                print(f'Directory: {os.path.abspath(neat_dir)}')
                
                with open(neat_dir + '/tomoe.html', 'x', encoding="utf-8") as f:
                    f.write('<html><center><body>')
                    f.write(f"<h1>{neat_dir}</h1>")

                    for i in nums(1, len(img)):
                        
                        f.write(f'<img src="{neat_dir}/{i}.jpg"><p></p>')
                    f.write(f'{project()}')
                    f.write('</body></center></html>')
                    f.close()

                try:
                    desired = inputimeout(prompt='Do you want to render it all to .pdf? (y/n) ', timeout=10)
                    to_pdf = desired

                    if to_pdf == 'y':
                        try:
                            source = open(f"{neat_dir}/tomoe.html")
                            output = f"{neat_dir}/{set_name}.pdf"
                            filepdf = output.rsplit('/', 1)[-1]

                            convert_html_to_pdf(source, output)
                            print(f'Successfully rendered to {filepdf} | {get_size(output)} MB') 
            
                        except Exception as e:
                            print(f"Something went wrong while converting to pdf: {e}")
                                
                    elif to_pdf == 'n':
                        print("Okay")
                        os.remove(neat_dir + '/tomoe.html')
                        return

                    else:
                        print("Invalid input")
                        os.remove(neat_dir + '/tomoe.html')
                        return

                except TimeoutOccurred:
                    print("Timeout occurred")
                    os.remove(neat_dir + '/tomoe.html')
                    exit()
