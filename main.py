import json
import time
from urllib import parse
# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests



BASE_URL = 'https://megamarket.ru'

def get_pagees_html(url):
    options = webdriver.ChromeOptions()
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

    response = requests.get(url)
    print(response.status_code)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with webdriver.Chrome() as driver:
        driver.get(url)
        time.sleep(1)
        p_tags = driver.find_element(By.ID, "scroll-container").find_elements(By.TAG_NAME, "p")

def get_items(html, items):
    pass

def save_excel(data: list, filename: str):
    pass


def main():
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
    print(target_url)
    items = get_pagees_html(url=target_url)


if __name__ == "__main__":
    main()