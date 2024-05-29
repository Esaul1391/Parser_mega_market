import json
import time
from urllib import parse
# import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests

BASE_URL = 'https://megamarket.ru'


def get_target_url():
    """
    Добавить поиск слов с пробелами
    """
    # target = input('Введите название товара: ')
    # min_price = input('Какая минимальная цена на товар')
    # min_price = min_price if min_price != '' else '0'
    # max_price = input('Какя максимальная цена на товар')
    # max_price = max_price if max_price != '' else '999999'
    target = 'lada_granta'
    min_price = '10'
    min_price = min_price if min_price != '' else '0'
    max_price = '20000'
    max_price = max_price if max_price != '' else '999999'
    target_url = f'{BASE_URL}/catalog/page_num/?q={target}'
    if max_price and min_price and (max_price.isdigit() and min_price.isdigit()):
        filter_price_count = {
            "88C83F68482F447C9F4E401955196697": {"min": int(min_price), "max": int(max_price)},
            "4CB2C27EAAFC4EB39378C4B7487E6C9E": ["1"]
        }
        json_data = json.dumps(filter_price_count)
        url_encode_data = parse.quote(json_data)
        target_url += '#?filters=' + url_encode_data
    return target_url


def get_pages_html(url):
    """
    Получаю url, проверяю доступность сайта, загружаю нужные параметры
    """
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument(f"user-agent={useragent.random}")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')
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


def parse_page(driver):
    pagination_frame = driver.find_element(By.TAG_NAME, 'body')

    # scroll_to_element(driver, pagination_frame)
    time.sleep(1)

def get_items(html, items):
    pass


def save_excel(data: list, filename: str):
    pass


def scroll_to_element(driver, element):
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # driver.execute_script("arguments[0].scrollIntoView();", element)

    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()


def main():
    target_url = get_target_url()
    print(target_url)
    get_driver = get_pages_html(target_url)
    parse_page(get_driver)
    time.sleep(1)


if __name__ == "__main__":
    main()
