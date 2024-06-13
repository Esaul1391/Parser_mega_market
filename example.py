import json
import time
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

BASE_URL = 'https://megamarket.ru'


def get_target_url():
    """
        Добавить поиск слов с пробелами
        """
    target = 'lada_granta'
    min_price = '10'
    max_price = '1000'
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


def get_items(cart):
    id = cart.find_element(By.CSS_SELECTOR, '[data-test="product-id"]').text
    name = cart.find_element(By.CSS_SELECTOR, '[data-test="product-name-link"]').text
    price = cart.find_element(By.CSS_SELECTOR, '[data-test="product-price"]').text
    link = cart.find_element(By.CSS_SELECTOR, '[data-test="product-name-link"]').get_attribute('href')
    try:
        discount = cart.find_element(By.CSS_SELECTOR, '[data-test="bonus-percent"]').text
    except:
        discount = None
    try:
        bonus = cart.find_element(By.CSS_SELECTOR, '[data-test="bonus-amount"]').text
    except:
        bonus = None
    cart_dict = {
        'id': id,
        'name': name,
        'price': price,
        'link': link,
        'discount': discount,
        'bonus': bonus
    }

    return cart_dict


def parse_page(driver):
    for i in range(1):  # Вы можете изменить количество страниц для парсинга
        pagination_frame = driver.find_element(By.CLASS_NAME, 'full')
        scroll_to_element(driver, pagination_frame)
        time.sleep(1)
        body = driver.find_element(By.CLASS_NAME, 'catalog-items-list')
        carts = body.find_elements(By.CSS_SELECTOR, '.catalog-item-regular-desktop')

        for cart in carts:
            """
            сделать проверку на наличие бонусов
            """
            print(get_items(cart))

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


def scroll_to_element(driver, element):  # как передивигать блоки
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()


def select_func(values):
    """
    Логика выбора лучших вариантов цены и бонусов
    """
    pass

def add_csv(values: dict):
    """
    Создаю csv файл и добавляю в него интересующие сочетания
    в дальнейшем переношу все в базу данных
    """
    pass


def main():
    target_url = get_target_url()
    print(target_url)

    with get_pages_html(target_url) as driver:
        parse_page(driver)


if __name__ == "__main__":
    main()
