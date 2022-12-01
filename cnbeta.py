import requests
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup


SERVER_NAME = 'https://x.liuping.win'

# proxies =  {
#    'http': 'http://127.0.0.1:10809',
#    'https': 'http://127.0.0.1:10809',
# }
proxies = None

hot_headers = {
    'authority': 'hot.cnbeta.com.tw',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'Host': 'hot.cnbeta.com.tw',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

headers = {
    'authority': 'www.cnbeta.com.tw',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'Host': 'www.cnbeta.com.tw',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

def parse_img(url):
    print('-----img')
    r = requests.get(url)
    p = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest() + url[url.rindex('.'):]
    with open(sys.path[0] + '/img/' + p, 'wb') as f:
        f.write(r.content)
    return SERVER_NAME + '/img/' +  p

def parse_artical(url):
    print('-----artical')
    print(url)
    p = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest() + url[url.rindex('.'):]
    if not Path(sys.path[0] + '/artical/' + p).exists():
        r = None
        if url.startswith('//hot.cnbeta.com.tw'):
            url = 'https:' + url
            r = requests.get(url, headers=hot_headers, proxies=proxies)
        else:
            r = requests.get(url, headers=headers, proxies=proxies)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.select_one('.cnbeta-article > header > h1').string
        print('title:', title)
        summary = soup.select_one('.article-summary > p')
        content = soup.select_one('.article-content')
        for one in content.select('.article-topic'):
            one.decompose()
        for a in content.select('a'):
            for one in a.children:
                a.insert_before(one)
            a.decompose()
        for img in content.select('img'):
            img['src'] = parse_img(img['src'])
            if img.parent.name == 'a' and img.parent.has_attr('href'):
                img.parent['href'] = img['src']
        with open(sys.path[0] + '/artical/' + p, 'w+', encoding='utf-8') as f:
            f.write('<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>' + title + '</title><style>img {max-width: 90%;} body {text-align: center;}</style></head><body>' + '<h1>' + title + '</h1>' + str(summary) + '<hr>' + str(content) + '</body></html>')
    return SERVER_NAME + '/artical/' + p


def parse_index():
    r = requests.get('https://www.cnbeta.com.tw/', headers=headers, proxies=proxies)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    items = []
    for item in soup.select('.item'):
        a = item.select_one('dl > dt > a')
        if a is not None and a.has_attr('href'):
            a['href'] = parse_artical(a['href'])
            del a['target']
            items.append(str(a))
    articals = '<br/>'.join(items)
    s = '<p>' + (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') + '</p>'
    with open(sys.path[0] + '/index.html', 'w+', encoding='utf-8') as f:
        f.write(f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><title>cnbeta</title></head><body>{s}{articals}</body></html>')
        

if __name__ == '__main__':
    parse_index()