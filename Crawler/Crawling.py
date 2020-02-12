from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
from saver import *
from selenium import webdriver
from requests.exceptions import Timeout, RequestException
from multiprocessing import Pool

import requests

PATH = "./webdriver/chromedriver"


def set_chrome_browser():
    """ Load chrome browser function.

    :return: Chrome browser Object.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument('headless')  # headless 모드 설정
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # 속도 향상을 위한 옵션 해제
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                        'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(PATH, options=options)

    return browser


def apply_multiprocessing(func, data, **kwargs) -> list:
    workers = kwargs.pop("workers")

    pool = Pool(processes=workers)
    result = pool.map(func, data)
    pool.close()

    return result


def get_content(link) -> str:
    """ Get Article content.

        :param link: Article Url.
        :return: Article content.
        """
    body = ""

    try:
        response = requests.get(link)
        response.encoding = None
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        for content in soup.find_all("div", {"class": "par"}):
            # [s.extract() for s in content("제거할 태그"})]
            # 해당 태그 삭제
            [s.extract() for s in content("script")]
            [s.extract() for s in content("span")]
            [s.extract() for s in content("a", {"target": "_blank"})]

            body += content.text
    except Timeout as e:
        print(e)
        return None
    except RequestException as e:
        print(e)
        return None

    print(f"content: \n{body}\n")
    return body


def get_data(url):
    driver = set_chrome_browser()
    titles = []
    views = []
    article_link = []
    contents = []

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for title_tag in soup.select('dt > a > span'):
        titles.append(title_tag.text)
        print(f"title: \n{title_tag.text}\n")

    for view_tag in soup.select('div > em'):
        views.append(view_tag.text)
        print(f"views: \n{view_tag.text}\n")

    for link_tag in soup.select('div > dt > a'):
        link = "https:" + link_tag["href"]
        article_link.append(link)
        print(f"link: \n{link}\n")

    # 병렬처리
    contents = apply_multiprocessing(get_content, article_link, workers=4)

    # convert views string to int
    views = list(map(lambda x: int("".join(x.split(","))), views))

    return titles, views, article_link, contents

