import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from additionally import scroll_to_element, add_csv


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
