#
# * S-Name:		archivach-downloader
# * Author:		Sflashy#7643 - sflashy@mail.com
# * Date:		01/08/2021
#

import sys, re, os
from datetime import datetime
from uuid import uuid4
from multiprocessing.pool import ThreadPool
try:
    import requests
except:
    sys.exit(f'{str(datetime.now())[:-7]} INFO Please run the it again!')


class Arhivach:
    THREADS = 10
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}

    def __init__(self):
        self.session = requests.Session()
        self.threadId = sys.argv[1]
        self.imageList = []

    def fetchImages(self):
        htmlResponse = self.session.get(f'http://arhivach.net/thread/{self.threadId}')
        if htmlResponse.status_code == 200:
            for image in re.findall(r"http(.*?)','.*','.*',event", htmlResponse.text):
                self.imageList.append('https' + image)
        else:
            print(f'{str(datetime.now())[:-7]} ERROR Cannot connect to the server [{htmlResponse.status_code}]')

    def mkdir(self):
        if not os.path.exists('./downloads'):
            os.mkdir('./downloads')

    def downloadImages(self, url):
        fileExt = re.search(r'(\.mp4|\.gif|\.jpg|\.png|\.webm|\.jpeg)', url).group(1)
        fileName = uuid4().hex
        print(f'{str(datetime.now())[:-7]} INFO Downloading: {fileName}{fileExt}    ', end='\r')
        htmlResponse = self.session.get(url)
        while htmlResponse.status_code != 200:
            print(f'{str(datetime.now())[:-7]} INFO RETRYING: {fileName}{fileExt}   ', end='\r')
            htmlResponse = self.session.get(url)
        with open('./downloads/' + fileName + fileExt, 'wb') as f:
            f.write(htmlResponse.content)


print(f'{str(datetime.now())[:-7]} INFO Initializing...')
archivach = Arhivach()
archivach.mkdir()
print(f'{str(datetime.now())[:-7]} INFO Fetching images...')
archivach.fetchImages()

try:
    _ = [_ for _ in ThreadPool(archivach.THREADS).imap_unordered(archivach.downloadImages, archivach.imageList)]
except:
    print(f'{str(datetime.now())[:-7]} INFO Operation terminated by user            ')
