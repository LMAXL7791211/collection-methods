# 1.Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
# а не по IATA коду. (У aviasales есть для этого дополнительное API) Пункт отправления и пункт
# назначения должны передаваться в качестве параметров. Сделать форматированный вывод, который
# содержит в себе пункт отправления, пункт назначения, дату вылета, цену билета (можно добавить
# еще другие параметры по желанию)
# + ввод от пользователя
# + API по IP адресу
# + замечания, доработки (сортировка, функции, белый ip)

# программа по википедии приклеена снизу



from pprint import pprint
import requests
import json
import dns.resolver  # $ pip install dnspython
import time

serviceCity = 'https://www.travelpayouts.com/widgets_suggest_params?'
# пример: q=Из%20Москвы%20в%20Лондон
# link = f'{serviceCity}q=Из%20{fromCityName}%20в%20{toCityName}'
# qua = 'москва афины'


def get_data(link, autoOrig):
    req = requests.get(link)
    if autoOrig:
        return json.loads(req.text[9:-2])
    else:
        return json.loads(req.text)


def getuserip():
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["208.67.222.222", "208.67.220.220"]
    return resolver.query('myip.opendns.com')[0]

ip = getuserip()
print(f'Ваш IP = {ip}')

serviceCityAutoOrig = 'http://www.travelpayouts.com/whereami?locale=ru&callback=useriata'
linkAutoOrig = f'{serviceCityAutoOrig}&ip={ip}'
dataAutoOrig = get_data(linkAutoOrig, True)
#  pprint(dataAutoOrig)

fromCity = dataAutoOrig['iata']
fromCityName = dataAutoOrig['name']

choiceOrig = input(f'Летите из города {fromCityName}? (введите y если да)')

data = {}
while data == {}:
    if choiceOrig == 'y':
        qua = input('Введите пункт назначения, например: Лондон')
        link = f'{serviceCity}q={fromCityName} {qua}'
    else:
        qua = input('Введите пункт отправления и назначения, например: Москва Лондон')
        link = f'{serviceCity}q={qua}'
    data = get_data(link, False)
    pprint(data)
    if data == {}:
        if choiceOrig == 'y':
            print('Не удалось распознать пункт назначения, введите, пожалуйста, еще раз (на русском языке)')
        else:
            print('Не удалось распознать пункты, введите, пожалуйста, еще раз два пункта по русски через пробел')

fromCity = data['origin']['iata']
toCity = data['destination']['iata']
fromCityName = data['origin']['name']
toCityName = data['destination']['name']

service = 'http://min-prices.aviasales.ru/calendar_preload?'
link = f'{service}origin={fromCity}&destination={toCity}&one_way=true'
data = get_data(link, False)

prices = []
for i in data['best_prices']:
    prices.append((i['value'], i['depart_date'], i['gate']))

# сортировка по цене, а при одинаковой цене - по дате
prices.sort(key=lambda x: (x[0], time.strptime(x[1], '%Y-%m-%d')))


print(f"\n Лучшие цены на билеты {fromCityName}({fromCity})-{toCityName}({toCity}):\n")

for i in prices:
    print(f"вылет {i[1]}, цена: {i[0]}, сервис: {i[2]}")

# конец решения задачи 1 авиасейлс.
# ------------------------------------

#     2.В приложении парсинга википедии получить первую ссылку из раздела "Ссылки"
#  и вывести все значимые слова из неё. Результат записать в файл в форматированном виде.
#
# 3.* Научить приложение определять количество ссылок в статье (раздел Ссылки).
# Выполнить поиск слов в статьях по каждой ссылке и результаты записать в отдельные файлы.

from pprint import pprint
import requests
import re


def get_link(topic, wikiornot):
    if wikiornot:
        link = 'https://ru.wikipedia.org/wiki/'+topic.capitalize()
    else:
        link = topic
    return link


def get_topic_page(topic, wikiornot):
    link = get_link(topic, wikiornot)
    html = requests.get(link).text
    return html


def get_topic_text(topic, wikiornot):
    html_content = get_topic_page(topic, wikiornot)
    words = re.findall("[а-яА-Яё]{3,}",html_content)
    #text = ' '.join(words)
    return words


def get_common_words(topic, wikiornot):
    words_list = get_topic_text(topic, wikiornot)
    rate = {}
    for word in words_list:
        if word in rate:
            rate[word] += 1
        else:
            rate[word] = 1
    rate_list = list(rate.items())
    rate_list.sort(key=lambda x: -x[1])
    return rate_list

# dict1 = get_common_words('Дерево')
# pprint(dict1)

# text = get_topic_text('Дерево')
# print(len(text))
# print(text[0:1000])


topic = 'Россия'

page = get_topic_page(topic, True)
# print(len(page))
# print(page[:10000])

links_section = re.findall('id="Ссылки"[\s\S]*', page)[0]
# print(links_section)

links = re.findall('<li><a rel="nofollow" class="external text" href="(.+?)">', links_section)
pprint(links)
print(f'Всего в разделе {len(links)} ссылок')

for i, link in enumerate(links):
    words = get_common_words(link, False)
    print(words)
    with open(topic.capitalize() + 'link' + str(i + 1) + '.txt', 'w', encoding='utf-8') as f:
        f.write(str(words))
