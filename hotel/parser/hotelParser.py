import json
from bs4 import BeautifulSoup
import requests



class TravelParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept-Language': 'ru',
        }

    def parse_block(self, item):
        content = {}
        # Название отеля
        div_title = item.find('div', {'class': 'item-content'})
        title = div_title.find('h2').get_text()
        title = title.replace('\n', '')
        # Цена номера
        try:
            prices = item.find('div', {'class': 'item-price'})
            price = prices.get_text()
            price = price.replace(' ', '').replace('\n', '').replace('\r', '').replace('от', "от ")
        except Exception:
            price = 'нет данных'
        # Адрес
        try:
            address = item.find('span', {'class': 'item-address'}).get_text()
            from_center = item.find('span', {'class': 'distance tooltip'}).get_text()
            address = address + ' '+ from_center
        except Exception:
            address = 'Нет данных'
            # Подробнее
        # try:
        #     href = item.find('div', {'class': 'item-bottom'}).find('div', {'class': 'pull-right'}).find('a').attrs['href']
        # except Exception:
        #     href = 'Нет данных'

        content.update(
            {'Title': title,
             'Price': price,
             'Address': address
             })

        return content

    def get_page(self, page: int = None):
        params = {}
        if page and page > 1:
            params['page='] = page

        # html = self.session.get(
        #     "https://101hotels.com/main/cities/sankt-peterburg/mini?adults=2&unknown_date=1",
        #     params=params)
        #
        # with open("text.html", 'w', encoding='utf-8') as f:
        #     f.write(html.text)
        with open("text.html", encoding='utf-8') as f:
            src = f.read()

        return src

    def get_content(self):
        html = self.get_page(1)
        cn = []
        bs = BeautifulSoup(html, features='lxml')
        blocks = bs.find('ul', {'class': 'unstyled clearfix hotellist grid'}).findAll('li', {'class': 'item'})
        for block in blocks:
            content = self.parse_block(block)
            cn.append(content)
        return cn


def parse_hotels():
    a = TravelParser()
    cn = a.get_content()
    return cn


