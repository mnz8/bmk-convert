# pip3 install requests

# doesn't work

import requests
from bs4 import BeautifulSoup
import os

with open(os.path.join(os.getcwd(), 'link.md')) as f:
    line = f.readline()
    while line:
        # 去掉空行
        if line.isspace():
            line = f.readline()
        else:
            # 去掉行尾换行符
            href = line.strip('\n')
            res = requests.get(href)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'lxml')
            print(soup.title.text)
            line = f.readline()