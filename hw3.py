# Здесь будет ДЗ к уроку 3 курса "Методы сбора"

# 1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика
#  с сайта superjob.ru или hh.ru. (Можно с обоих сразу)
#  Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе:
# • Наименование вакансии,
# • Предлагаемую зарплату,
# • Ссылку на саму вакансию
#
# 2) Доработать приложение таким образом, чтобы можно было искать разработчиков на разные языки
#  программирования (Например Python, Java, C++)

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from time import sleep
from random import randint

PAGES = 3
PROFESSION = 'Программист%20JavaScript'
vacs = []


def vacblock(html):
    parsed_html = bs(html, 'html.parser')
    # pprint(link)
    # pprint(bs.findChildren(link))
    vaclist = parsed_html.find(name='div', attrs={'style': "display:block"})
#    pprint(vaclist)
    if vaclist is not None:
        return vaclist.find_all(name='div', attrs={'class': "_212By _37XTu"})
    else:
        return []


for i in range(PAGES):
    if i == 0:
        html = requests.get('https://www.superjob.ru/vacancy/search/?keywords=' + PROFESSION + '&geo%5Bc%5D%5B0%5D=1').text
    else:
        html = requests.get('https://www.superjob.ru/vacancy/search/?keywords=' + PROFESSION + '&geo%5Bc%5D%5B0%5D=1&page=' + str(i+1)).text

    # with open('sj.htm', 'w', encoding='utf-8') as f:
    #    f.write(html)

    # with open('sj.htm', 'r', encoding='utf-8') as f:
    #     html = f.read()

    # pprint(html[1000:3000])
    vacblocks = vacblock(html)
    print(f'Page {i+1}, {int(len(vacblocks) / 2)} positions on page')
    if len(vacblocks) == 0:
        break
    for block in vacblocks:
        if vacblocks.index(block) % 2 == 1:
            vacs.append({'vacname': block.find(name='div', attrs={'class': "_3mfro CuJz5 PlM3e _2JVkc _3LJqf"}).text,
                         'salary': block.find(name='span', attrs={'class': re.compile(r"salary*")}).text.replace(u'\xa0', ' '),
                         'link': 'https://www.superjob.ru' + block.find(name='a', href=re.compile(r"/vakansii*"))['href']})
    sleep(4 + randint(0, 4))

pprint(vacs)
print(f'{len(vacs)} total positions.')

