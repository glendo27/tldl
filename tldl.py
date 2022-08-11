import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
session = requests.session()

if "--tor" in sys.argv:
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    sys.argv.remove("--tor")

for argv in sys.argv[1:]:
    url = f"https://nitter.42l.fr/{argv}/media"
    download = True
    print(f"Downloading: {argv}")     
    while download:
        url_data = session.get(url, headers=headers)
        if url_data.ok: 
            soup = BeautifulSoup(url_data.text, "html.parser")           
            if soup.find(class_="profile-card-username"):
                raw_username = soup.find(class_="profile-card-username").get_text()       
                username = raw_username.replace("@", "")

            for link in soup.find_all("a", class_="still-image"):            
                if "/pic/orig/media" in link.get("href"):
                    image_url = f"https://nitter.42l.fr{link.get('href')}"
                    image_name = link.get('href').replace('/pic/orig/media%2F', 'media_')
                    response = session.get(image_url, stream=True)
                    if not os.path.exists(username):
                        os.mkdir(username)
                    running_dir = os.listdir(os.path.abspath(f"{os.getcwd()}/{username}"))
                    if not image_name in running_dir:
                        with open(f'{username}/{image_name}', 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                            print(f"Downloaded: {image_url}")
                        del response
                    else:
                        print(f"Exist image: {image_url}")
            
            if soup.find("a", string="Load more"):
                href = soup.find("a", string="Load more").get('href')
                url = f"https://nitter.42l.fr/{username}/media/{href}"
                print(f"Getting next page: {url}")
            else:
                download = False
                print(f"Downloading complete: '{argv}'")
        else:
            download = False
            print(f"Url not avaliable: {url}\nSkiping next")
