from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient
import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

client = MongoClient('localhost', 27017)
db = client['news_database']
news_db_lenta = db.lenta

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = 'https://lenta.ru/'

response = requests.get(url, headers=header)
pprint(response.status_code)
dom = html.fromstring(response.text)
#newsss = dom.xpath('//div[@class="item"]')
newsss = dom.xpath('//time[@class="g-time"]/../..')
newsss_list = []
for news in newsss:
     news_content = {}
     name = ''.join(news.xpath(".//a/text()")).replace('\xa0', ' ')
     link = news.xpath(".//a/@href")
     link = url+link[0][1:]

     date = ''.join(news.xpath(".//a/time/@datetime")).replace('ноября', '11')[1:]
     date_time = datetime.strptime(date, '%H:%M, %d %m %Y')

     news_content['name'] = name
     news_content['link'] = link
     news_content['date'] = date_time

     newsss_list.append(news_content)

     newsss_dict = {'name': name, 'link': link, 'date': date_time, 'sourse-link': url}
     news_db_lenta.insert_one(newsss_dict)

pprint(newsss_list)



