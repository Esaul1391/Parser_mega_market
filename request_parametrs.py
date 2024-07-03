import json
from urllib import parse

BASE_URL = 'https://megamarket.ru'


def request_param(target=None, count_page=1, min_price='10', max_price='100000'):
    if not target:
        target = input('Поисковой запрос: ')
    if count_page == 1:
        count_page = int(input('Число страниц для парсинга: '))
    if min_price == '10':
        min_price = str(input('Минимальная цена: '))
    if max_price == '100000':
        max_price = str(input('Максимальная цена: '))

    param = {
        'target': target,
        'count_page': count_page,
        'min_price': min_price,
        'max_price': max_price
    }
    return param


def get_target_url(target, min_price, max_price):
    """
        Добавить поиск слов с пробелами
        """
    target = target.replace(" ", "%20") if " " in target else target

    target_url = f'{BASE_URL}/catalog/page_num/?q={target}'
    if max_price and min_price and (max_price.isdigit() and min_price.isdigit()):
        filter_price_count = {
            "88C83F68482F447C9F4E401955196697": {"min": int(min_price), "max": int(max_price)},
            "4CB2C27EAAFC4EB39378C4B7487E6C9E": ["1"]
        }
        json_data = json.dumps(filter_price_count)
        url_encode_data = parse.quote(json_data)
        target_url += '#?filters=' + url_encode_data
        print(target_url)
    return target_url
