import sys
import ssl
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path

TARGETS = ['60_60910',]

def parse_one(url):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers('ALL')
    print(url)
    if '55067475.html' in url:
        url = '/60_60910/55067475.html?__HY=37102b604f36fac18bbfddda8cb183ada1666778764_1154397'
    with urllib.request.urlopen('https://www.74wx.com' + url ,context=context) as f:
        source = str(f.read(), 'gbk')
        soup = BeautifulSoup(source, 'html.parser')
        content = soup.select_one('#content')
        if content is not None:
            with open(sys.path[0] + url, 'w+', encoding='utf-8') as w:
                w.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>唐人的餐桌</title></head><body>{str(content)}</body></html>')
    


def parse_index(target: str):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers('ALL')
    with urllib.request.urlopen('https://www.74wx.com/' + target + '/', context=context) as f:
        path = Path(sys.path[0] + '/' + target)
        files = [x.name for x in path.iterdir() if x.is_file()]
        source = str(f.read(), 'gbk')
        soup = BeautifulSoup(source, 'html.parser')
        for a in soup.select('dl > dd > a')[:10]:
            href = a['href']
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
        
