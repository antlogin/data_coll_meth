from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_database']
news_db_lenta = db.lenta

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = 'https://lenta.ru/'

response = requests.get(url, headers=header)
pprint(response.status_code)
dom = html.fromstring(response.text)
newsss = dom.xpath('//div[@class="item"]')

newsss_list = []
for news in newsss:
     news_content = {}
     name = news.xpath(".//a/text()")
     name[0] = name[0].replace('\xa0', ' ')
     link = news.xpath(".//a/@href")
     link[0] = url+link[0][1:]
     date = news.xpath(".//a/time/@datetime")

     news_content['name'] = name
     news_content['link'] = link
     news_content['date'] = date

     newsss_list.append(news_content)

     newsss_dict = {'name': name, 'link': link, 'date': date, 'sourse-link': url}
     news_db_lenta.insert_one(newsss_dict)

pprint(newsss_list)



