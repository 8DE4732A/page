import sys
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path

TARGETS = ['60_60910',]

def parse_one(url):
    with urllib.request.urlopen('https://www.74wx.com' + url ) as f:
        source = str(f.read(), 'gbk')
        soup = BeautifulSoup(source, 'html.parser')
        content = str(soup.select_one('#content'))
        if content:
            with open(sys.path[0] + url, 'w+', encoding='utf-8') as w:
                w.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>唐人的餐桌</title></head><body>{content}</body></html>')
    


def parse_index(target: str):
    with urllib.request.urlopen('https://www.74wx.com/' + target + '/') as f:
        path = Path(sys.path[0] + '/' + target)
        files = [x.name for x in path.iterdir() if x.is_file()]
        source = str(f.read(), 'gbk')
        soup = BeautifulSoup(source, 'html.parser')
        for a in soup.select('dl > dd > a')[:10]:
            href = a['href']
            if href[href.rfind('/') + 1:] not in files:
                try:
                    parse_one(href)
                except:
                    pass
        dl = str(soup.select_one('dl'))
        with open(sys.path[0] + '/' + target + '/index.html', 'w+', encoding='utf-8') as w:
            w.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>唐人的餐桌</title></head><body>{dl}</body></html>')

if __name__ == '__main__':
    for target in TARGETS:
        parse_index(target)
        