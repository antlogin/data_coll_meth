#https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&from=suggest_post&area=1&schedule=remote&search_field=description&search_field=company_name&search_field=name
#https://hh.ru/search/vacancy?text=%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&area=1&salary=&currency_code=RUR&experience=doesNotMatter&schedule=remote&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true
#&page=0-3
import numpy as np
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['hh_database']
hh_vacance_Mongo = db.hh_vacance_collection

hh_data = pd.DataFrame(columns={'name', 'link', 'max_salary', 'min_salary', 'salary_currency', 'site-link'})
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
pages = {'&page=0', '&page=1','&page=2','&page=3','&page=4', '&page=5','&page=6','&page=7', '&page=8', '&page=9','&page=10'}
#pages = {'&page=0'}
url='https://hh.ru/search/vacancy?text=%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&area=1&salary=&currency_code=RUR&experience=doesNotMatter&schedule=remote&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true'

for page in pages:
    response = requests.get(url+page, headers=headers)
    dom = BeautifulSoup(response.text,'html.parser')
    vacances = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacance in vacances:
        vacance_name = vacance.find('a', {'class': 'bloko-link'}).getText()
        vacance_link = vacance.find('a', {'class': 'bloko-link'}).get('href')
        try:
            vacance_salary = vacance.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            vacance_salary = vacance_salary.replace('\u202f', '')
            vacance_salary_currency = vacance_salary[vacance_salary.rindex(' ') + 1:]
            if vacance_salary[0] == 'о':
                vacance_salary_min = float(vacance_salary.split(" ")[1])
            else:
                if vacance_salary[0] == 'д':
                    vacance_salary_max = float(vacance_salary.split(" ")[1])
                else:
                    vacance_salary_min = float(vacance_salary.split(" ")[0])
                    vacance_salary_max = float(vacance_salary.split(" ")[2])
        except:
            vacance_salary_min = None
            vacance_salary_max = None
            vacance_salary_currency = None
        hh_data_dict = {'name': vacance_name, 'link': vacance_link, 'min_salary': vacance_salary_min,
                                   'max_salary': vacance_salary_max, 'salary_currency': vacance_salary_currency,
                                   'site-link': 'hh.ru'}
        hh_data = hh_data.append([hh_data_dict], ignore_index=True)  # hh_data = pd.DataFrame......

        if hh_vacance_Mongo.find_one({"name": vacance_name, 'link': vacance_link, 'min_salary': vacance_salary_min,
                                   'max_salary': vacance_salary_max, 'salary_currency': vacance_salary_currency}):
            pprint("Такая вакансия уже есть в базе")
        else:
            hh_vacance_Mongo.insert_one(hh_data_dict)
            pprint("Добавлена новая вакансия")
#pprint(hh_data[['min_salary', 'max_salary', 'salary_currency']].head(45))
pprint(f'Всего вакансий на сайте - {hh_data.shape[0]}')
pprint(f'Всего вакансий в базе - {hh_vacance_Mongo.count_documents({})}')


