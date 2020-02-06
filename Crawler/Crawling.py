from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
from saver import *
from selenium import webdriver

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


def get_content(link):
    """ Get Article content.

        :param link: Article Url.
        :return: Article content.
        """
    body = ""
    driver = set_chrome_browser()

    try:
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for content in soup.find_all("div", {"class": "par"}):
            body += content.text
    except TimeoutException as e:
        print(e)
        return None
    except WebDriverException as e:
        print(e)
        return None

    driver.close()

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
        content = get_content(link)
        contents.append(content)

        print(f"link: \n{link}\n")
        print(f"content: \n{content}\n")

    # convert views string to int
    views = list(map(lambda x: int("".join(x.split("m"))), views))

    return titles, views, article_link, contents

