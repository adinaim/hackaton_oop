import json
# import csv
import requests
from bs4 import BeautifulSoup
from utils import Body, Id
from pprint import pprint




class JSonMixin:
    file_name = 'cars.json'
    def get_db_data(self):
        try:
            with open(self.file_name, 'r') as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            return []

    def write_to_db(self, data):
        with open('cars.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)



class ParsingMixin(str):
    HOST = 'https://www.mashina.kg/search/all/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}


    def get_html(self, url, headers: dict='', params: str=''):
            html = requests.get(
                url,
                headers=headers,
                params=params,
                verify=False
            )
            return html.text



    def get_cards_from_html(self, html):
        """ Получение карточек авто """
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div', class_='list-item list-label') 
        return cards


    def parse_from_cards(self, cards):
        """ Фильтрация данных из карточек """
        result = []
        for card in cards:

            try:
                title = card.find('a').find('div', class_='block title').find('h2').text.strip()
                list_title = title.split()
                brand = list_title[0]
                model = ' '.join(list_title[1:])
            except AttributeError:
                brand = ''
                model = ''
                

            try:
                year = int(card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='year-miles').find('span').text.split(' ')[0].strip())
            except AttributeError:
                year = ''


            try:
                volume = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='year-miles').text.split(',')[-2].strip().split(' ')[0]
                if volume != '':
                    volume = float(volume)
                else:
                    volume = ''
            except AttributeError:
                volume = ''


            try:
                price = float(''.join(card.find('a').find('div', class_='block price').find('p').text.split('\n')[1].split(' ')[1:]))
            except AttributeError:
                price = ''


            try:
                color = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='year-miles').find('i').get('title')
            except AttributeError:
                color = ''


            try:
                body = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='body-type').text.split()[0].strip(',')
            except AttributeError:
                body = ''
            

            try:
                mileage = card.find('a').find('div', class_='block info-wrapper item-info-wrapper').find('p', class_='volume').text.split(',')
                if len(mileage) >= 2:
                    mileage = float(''.join(mileage[-1].strip().split(' ')[:-1]))
                else:
                    mileage = ''
            except AttributeError:
                mileage = ''


            parsed_car = {
                'id' : Id.generate_id(),
                'brand': brand,
                'model': model,
                'year': year,
                'volume': volume,
                'price': price,
                'color': color,
                'body': body,
                'mileage': mileage
            }

            result.append(parsed_car)
        return result


    def find_last_page(self):
        """ Получение количества страниц """
        html = self.get_html(self.HOST)
        soup = BeautifulSoup(html, 'lxml')
        total_pages = soup.find('div', class_='search-results-table').find('nav').find('ul', class_='pagination').find_all('li', class_='page-item')[-1]
        last_page = total_pages.find('a').get('data-page')
        return int(last_page)


    def main(self):
        result = []
        # for page in range(1, get_last_page(category)+1):
        for page in range(1, self.find_last_page()-953):
            html = self.get_html(self.HOST, params=f'page={page}', headers=self.HEADERS)
            cards = self.get_cards_from_html(html)
            list_of_cards = self.parse_from_cards(cards)
            result.extend(list_of_cards)
        JSonMixin.write_to_db(self, result)

if __name__ == '__main__':     
    obj = ParsingMixin()
    obj.main()




class CreateMixin:

    def create(self):
        model = self._model
        try:
            brand: str = input('Введите марку авто: ')
            model: str = input('Введите модель авто: ')
            year: int = input('Введите год выпуска авто: ')
            volume: float = input('Введите объем двигателя авто: ')
            color: str = input('Введите цвет авто: ')
            body = Body.choose_body(self)
            mileage: int = input('Введите пробег авто: ')
            price: float = input('Введите цену авто: ')
        except ValueError:
            print('Неправильный ввод. Повторите попытку')
            brand: str = input('Введите марку авто: ')
            model: str = input('Введите модель авто: ')
            year: int = input('Введите год выпуска авто: ')
            volume: float = input('Введите объем двигателя авто: ')
            color: str = input('Введите цвет авто: ')
            body = Body.choose_body(self)
            mileage: int = input('Введите пробег авто: ')
            price: float = input('Введите цену авто: ')

        car = {
                'id': Id.generate_id(),
                'brand': brand,
                'model': model,
                'year': year,
                'volume': volume,
                'color': color,
                'body': body,
                'mileage': mileage,
                'price': price
            }
        data = self.get_db_data()
        data.append(car)
        self.write_to_db(data)



class ListingMixin:
    def list(self):
        data = self.get_db_data()
        pprint(data)



class RetrieveMixin:
    def get_car_by_id(self):
        car_id = input('Введите id авто: ')
        data = self.get_db_data()
        res = list(filter(lambda x: x['id'] == car_id, data))
        pprint(res[0] if res else 'Не найдено')
        return res[0] if res else None



class UpdateMixin:
    def update(self):
        data = self.get_db_data()
        car = self.get_car_by_id()
        if car is not None:
            data.remove(car)
            id = car['id']
            brand: str = input('Введите марку авто: ') or car['brand']
            model: str = input('Введите модель авто: ') or car['model']
            year: int = input('Введите год выпуска авто: ') or car['year']
            volume: float = input('Введите объем двигателя авто: ') or car['volume']
            color: str = input('Введите цвет авто: ') or car['color']
            body = Body.choose_body(self) or car['body']
            mileage: int = input('Введите пробег авто: ') or car['mileage']
            price: float = input('Введите цену авто: ') or car['price']

            new_car = {
                'id': id,
                'brand': brand,
                'model': model,
                'year': year,
                'volume': volume,
                'color': color,
                'body': body,
                'mileage': mileage,
                'price': price
            }
            data = self.get_db_data()
            data.append(new_car)
            self.write_to_db(data)
            print('Успешно')
        else:
            print('Не найдено')



class DeleteMixin:
    def delete(self):
        data = self.get_db_data()
        car = self.get_car_by_id()
        if car is not None:
            data.remove(car)
            self.write_to_db(data)
            print('Успешно удален')
        else:
            print('Не найдено')


