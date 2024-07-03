import json
import csv
import os
import time
from datetime import datetime
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from parse_page import get_pages_html, parse_page
from request_parametrs import get_target_url, request_param

BASE_URL = 'https://megamarket.ru'
FLAG_CSV = 0

def request_param(target=None, count_page=1, min_price='10', max_price='100000'):
    # Запрашиваем только те значения, которые не были переданы
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


def get_pages_html(url):
    """
        Инициализирую WebDriver и открываю страницу
        """
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    return driver


def parse_page(driver, target, count_page=1):
    for i in range(count_page):
        pagination_frame = driver.find_element(By.CLASS_NAME, 'full')
        scroll_to_element(driver, pagination_frame)
        time.sleep(1)
        body = driver.find_element(By.CLASS_NAME, 'catalog-items-list')
        carts = body.find_elements(By.CSS_SELECTOR, '.catalog-item-regular-desktop')
        cart_dict = []
        for cart in carts:
            """
            делаю проверку на наличие бонусов и добавляю в словарь
            """
            cart_value = get_items(cart)
            if cart_value['bonus']:
                cart_dict.append(cart_value)
        add_csv(cart_dict, target)

        try:
            pagination_clik = driver.find_element(By.CLASS_NAME, 'next')
            if not pagination_clik.is_enabled():
                print('последняя страница')
                break
            pagination_clik.click()
            time.sleep(1)
        except Exception:
            print('Конец')
            break


def get_items(cart):
    id = int(cart.get_attribute('id'))
    name = cart.find_element(By.CSS_SELECTOR, '[data-test="product-name-link"]').text
    price = int(cart.find_element(By.CSS_SELECTOR, '[data-test="product-price"]').text.split(' ')[0])
    link = cart.find_element(By.CSS_SELECTOR, '[data-test="product-name-link"]').get_attribute('href')
    try:
        discount = cart.find_element(By.CSS_SELECTOR, '[data-test="bonus-percent"]').text
    except:
        discount = None
    try:
        bonus = int(cart.find_element(By.CSS_SELECTOR, '[data-test="bonus-amount"]').text)
    except:
        bonus = 0
    cart_dict = {
        'id': id,
        'name': name,
        'price': price,
        'bonus': bonus,
        'k': bonus / price,
        'discount': discount,
        'link': link,
    }

    return cart_dict


def scroll_to_element(driver, element):  # как передивигать блоки
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()


def add_csv(values: list, target: str):
    """
    Создаю csv файл и добавляю в него интересующие сочетания
    в дальнейшем переношу все в базу данных
    """
    file_name = f'{target}_{datetime.now().strftime("%d_%m_%Y")}.csv'  # прописать сюда название категории и дату
    with open(f'{file_name}', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not FLAG_CSV:
            writer.writerow(['id', 'name', 'price', 'bonus', 'k', 'discount', 'link'])

        for value in values:
            writer.writerow(value.values())


def main():
    dict_param = request_param()
    target_url = get_target_url(dict_param['target'], dict_param['min_price'], dict_param['max_price'])
    print(target_url)

    with get_pages_html(target_url) as driver:
        parse_page(driver, dict_param['target'], dict_param['count_page'])


if __name__ == "__main__":
    main()
