import requests
import sys
from bs4 import BeautifulSoup

SERVER_NAME = 'https://xs.liuping.win/cnbeta'

def parse_index():
    headers = {
        'authority': 'www.cnbeta.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'Host': 'www.cnbeta.com',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    }
   
    r = requests.get('https://www.cnbeta.com/', headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    items = []
    for item in soup.select('.item'):
        a = item.select_one('dl > dt > a')
        if a is not None and a.has_attr('href'):
            a['href'] = a['href'].replace('https://www.cnbeta.com.tw', SERVER_NAME).replace('//hot.cnbeta.com.tw', SERVER_NAME + '/hot')
            del a['target']
            items.append(str(a))
    articals = '<br/>'.join(items)
    with open(sys.path[0] + '/cnbeta/index.html', 'w+', encoding='utf-8') as f:
        f.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>cnbeta</title></head><body>{articals}</body></html>')
        

if __name__ == '__main__':
    parse_index()