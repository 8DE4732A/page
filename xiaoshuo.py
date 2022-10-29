import sys
import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path

TARGETS = ['60_60910',]

def parse_one(url):
    r = requests.get('https://www.74wx.vip' + url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.select_one('#content')
    if content is not None:
        with open(sys.path[0] + url, 'w+', encoding='utf-8') as w:
            w.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>唐人的餐桌</title></head><body>{str(content)}</body></html>')
    


def parse_index(target: str):
    r = requests.get('https://www.74wx.vip/' + target + '/')
    r.encoding = 'gbk'
    path = Path(sys.path[0] + '/' + target)
    files = [x.name for x in path.iterdir() if x.is_file()]
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.select('dl > dd > a')[:5]:
        href = a['href']
        try:
            parse_one(href)
            time.sleep(10)
        except:
            pass
    dl = str(soup.select_one('dl'))
    with open(sys.path[0] + '/' + target + '/index.html', 'w+', encoding='utf-8') as w:
        w.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>唐人的餐桌</title></head><body>{dl}</body></html>')

if __name__ == '__main__':
    for target in TARGETS:
        parse_index(target)
        
