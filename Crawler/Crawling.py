from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
from saver import *

import requests
from datetime import datetime

PATH = "./webdriver/chromedriver"


def set_chrome_browser():
    """ Load chrome browser function.

    :return: Chrome browser Object.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    browser = webdriver.Chrome(
            "./webdriver/chromedriver", options=options)

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

    return titles, views, article_link, contents

