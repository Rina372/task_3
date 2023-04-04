import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json


def get_headers():
    Headers(browser='firefox', os='win').generate()


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


hh_main_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_main_html, features='lxml')

all_vacancies_list = soup.find(id='a11y-main-content')
vacancy = all_vacancies_list.find_all(class_='serp-item')

vacancy_description_list = []
for item in vacancy:
    vacancy_description = item.find(class_='bloko-header-section-3')
    description = vacancy_description.find('span').text
    if 'Django' in description and 'Flask' in description:
        vacancy_description_list.append(item)

vacancy = []
for word in vacancy_description_list:
    title = word.find('a', class_='serp-item__title').text
    link_tag = word.find('a', class_='serp-item__title')
    link = link_tag['href']
    try:
        salary_tag = word.find('span', class_='bloko-header-section-3')
        salary = salary_tag.text
    except Exception:
        salary = 'Не указана'
    company_tag = word.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company = company_tag.text
    city_tag = word.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
    city = city_tag.text

    vacancy.append({

        'Название': title,
        'Зарплата': salary,
        'Компания': company,
        'Город': city,
        'Ссылка': link

    })

pprint(vacancy)

with open('vacancy.json', 'w') as f:
    json.dump(vacancy, f, ensure_ascii=False)
