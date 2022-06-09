import json
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'user-agent': f'{ua.random}'}


def get_all_page(experience="noExperience"):
    response = requests.get(
        url=f"https://makhachkala.hh.ru/search/vacancy?experience={experience}&search_field=name&text=Flutter+developer&order_by=relevance&items_on_page=20",
        headers=headers
    )
    text = response.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)

    with open('index.html', encoding='utf-8') as file:
        page = file.read()

    soup = BeautifulSoup(page, 'lxml')
    all_vacancies = soup.find("h1", {"data-qa": "bloko-header-3", "class": "bloko-header-section-3"}).text.split()[0]
    page_calculation = int(all_vacancies) / 20
    all_page = 1 if page_calculation <= 1 else page_calculation.__ceil__()

    print(f'Найдено {all_vacancies} вакансий\n')

    return all_page, all_vacancies


def get_data(experience="noExperience", page=0):
    count = 0
    all_works = []
    all_info = []

    response = requests.get(
        url=f"https://makhachkala.hh.ru/search/vacancy?experience={experience}&search_field=name&text=Flutter+developer&order_by=relevance&items_on_page=20&page={page}",
        headers=headers
    )
    text = response.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(text)

    with open('index.html', encoding='utf-8') as file:
        page = file.read()

    soup = BeautifulSoup(page, 'lxml')
    all_hrefs = soup.find_all('a',
                              {"data-qa": "vacancy-serp__vacancy-title", "target": "_blank", "class": "bloko-link"})
    for item in all_hrefs:
        item_href = item.get('href')
        item_text = item.text.replace(' ', ' ')
        all_works.append(
            {
                "link": item_href,
                "vacancy": item_text
            }
        )

    print(f'Идет скачивание {len(all_works)} вакансий\n')

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(all_works, file, indent=4, ensure_ascii=False)

    for item in all_works:
        if count % 10 == 0:
            time.sleep(2)

        count += 1
        response = requests.get(url=item.get("link"), headers=headers)

        print(f"Идет скачивание: {count} вакансии")
        html = response.text

        with open(f'data/{count}.html', 'w', encoding='utf-8') as file:
            file.write(html)

        with open(f'data/{count}.html', encoding='utf-8') as file:
            page = file.read()

        soup = BeautifulSoup(page, 'lxml')

        # получение описания
        try:
            info = soup.find('div', {"class": "g-user-content", "data-qa": "vacancy-description"}).find_all('p')
            info_list = []
            for item in info:
                item_text = item.text
                info_list.append(item_text)
        except Exception:
            info_list = ['Для просмотра информации перейдите по ссылке']

        # получение должности
        try:
            job_title = soup.find('h1', {"data-qa": "vacancy-title", "class": "bloko-header-1"}).text
        except Exception as e:
            job_title = 'нет данных'

        # получение города
        try:
            location = soup.find('p', {"data-qa": "vacancy-view-location"})
            if location is not None:
                location = soup.find('p', {"data-qa": "vacancy-view-location"}).text
            else:
                location = soup.find('a', {"class": "bloko-link bloko-link_disable-visited",
                                           "data-qa": "vacancy-view-link-location"}).text
        except Exception as e:
            location = 'нет данных'

        # получение з/п
        try:
            money = soup.find("div", {"data-qa": "vacancy-salary"}).text.replace(' ', ' ')
        except Exception:
            money = 'нет данных'

        # получение названия компании
        try:
            company = soup.find("a", {"data-qa": "vacancy-company-name", "class": "bloko-link"}).text.replace(' ',
                                                                                                              ' ')
        except Exception:
            company = 'нет данных'

        # получение требований
        try:
            requirements = soup.find("div", class_="bloko-gap bloko-gap_bottom").find_all('p')
            requirements_list = []
            for item in requirements[:2]:
                item_text = item.text
                requirements_list.append(item_text)
        except Exception:
            requirements_list = 'нет данных'

        # получение ключевых навыков
        try:
            skil = soup.find("div", class_="bloko-tag-list").find_all('span')
            skils_list = []
            for item in skil:
                item_text = item.text.replace(' ', ' ')
                skils_list.append(item_text)
        except Exception:
            skils_list = 'нет данных'

        all_info.append(
            {
                "Должность": job_title,
                "Компания": company,
                "Требования": requirements_list,
                "З/П": money,
                "Город": location,
                "Описание": info_list,
                "Ключевые навыки": skils_list
            }
        )

    with open(f'data/result.json', 'w', encoding='utf-8') as file:
        json.dump(all_info, file, indent=4, ensure_ascii=False)


def main():
    start_time = time.time()
    get_data()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
