# 1.Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
# а не по IATA коду. (У aviasales есть для этого дополнительное API) Пункт отправления и пункт
# назначения должны передаваться в качестве параметров. Сделать форматированный вывод, который
# содержит в себе пункт отправления, пункт назначения, дату вылета, цену билета (можно добавить
# еще другие параметры по желанию)
# + ввод от пользователя
# + API по IP адресу


from pprint import pprint
import requests
import json
import socket

serviceCity = 'https://www.travelpayouts.com/widgets_suggest_params?'
# пример: q=Из%20Москвы%20в%20Лондон
# link = f'{serviceCity}q=Из%20{fromCityName}%20в%20{toCityName}'
# qua = 'москва афины'

ip = socket.gethostbyname(socket.getfqdn())
print(f'Ваш IP = {ip}')

serviceCityAutoOrig = 'http://www.travelpayouts.com/whereami?locale=ru&callback=useriata'
linkAutoOrig = f'{serviceCityAutoOrig}&ip={ip}'
reqAutoOrig = requests.get(linkAutoOrig)
dataAutoOrig = json.loads(reqAutoOrig.text[9:-2])
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
    req = requests.get(link)
    data = json.loads(req.text)
    pprint(data)
    if data == {}:
        print('Не удалось распознать пункты, введите, пожалуйста, еще раз два пункта по русски через пробел')

fromCity = data['origin']['iata']
toCity = data['destination']['iata']
fromCityName = data['origin']['name']
toCityName = data['destination']['name']

service = 'http://min-prices.aviasales.ru/calendar_preload?'
link = f'{service}origin={fromCity}&destination={toCity}&one_way=true'
req = requests.get(link)
data = json.loads(req.text)

for i in data['best_prices']:
    print(f"{fromCityName}({fromCity})-{toCityName}({toCity}), вылет {i['depart_date']},\
цена: {i['value']}, сервис: {i['gate']}")
