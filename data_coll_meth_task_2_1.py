#https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&from=suggest_post&area=1&schedule=remote&search_field=description&search_field=company_name&search_field=name
#&page=0-3
import numpy as np
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup


hh_data = pd.DataFrame(columns={'name', 'link', 'max_salary', 'min_salary', 'salary_currency', 'site-link'})
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
pages = {'&page=0', '&page=1','&page=2','&page=3'}
url='https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&from=suggest_post&area=1&schedule=remote&search_field=description&search_field=company_name&search_field=name'

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
        hh_data = hh_data.append([{'name': vacance_name, 'link': vacance_link, 'min_salary': vacance_salary_min,
                                   'max_salary': vacance_salary_max, 'salary_currency': vacance_salary_currency,
                                   'site-link': 'hh.ru'}], ignore_index=True)
pprint(hh_data[['min_salary', 'max_salary', 'salary_currency']].head(45))
pprint(hh_data.shape)

