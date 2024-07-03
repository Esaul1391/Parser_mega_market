from parse_page import get_pages_html, parse_page
from request_parametrs import get_target_url, request_param


def main():
    dict_param = request_param()
    target_url = get_target_url(dict_param['target'], dict_param['min_price'], dict_param['max_price'])
    print(target_url)

    with get_pages_html(target_url) as driver:
        parse_page(driver, dict_param['target'], dict_param['count_page'])


if __name__ == "__main__":
    main()
