import csv
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = 'https://megamarket.ru'
FLAG_CSV = False


def scroll_to_element(driver, element):  # как передивигать блоки
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()


def add_csv(values: list, target: str):
    """
    Создаю csv файл и добавляю в него интересующие сочетания
    в дальнейшем переношу все в базу данных
    """
    file_name = f'data/{target}_{datetime.now().strftime("%d_%m_%Y")}.csv'  # прописать сюда название категории и дату
    with open(f'{file_name}', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        global FLAG_CSV
        if not FLAG_CSV:
            writer.writerow(['id', 'name', 'price', 'bonus', 'k', 'discount', 'link'])
            FLAG_CSV = True
        for value in values:
            writer.writerow(value.values())
