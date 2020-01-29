from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException, InvalidSelectorException
from bs4 import BeautifulSoup

import pandas as pd
import datetime
import requests

PATH = "./webdriver/chromedriver"
URL = "http://news.chosun.com/ranking/list.html?type=&site=www&scode=star&term=&date="


def load_chrome_browser():
    """
    Load chrome brawser function. (to remove overlap code)
    :return: Chrome browser Object.
    """
    chrome_options = Options()
    browser = webdriver.Chrome(
        "./webdriver/chrome/chromedriver", options=chrome_options)
    browser.set_window_size(1920, 1280) # 윈도우 사이즈를 맞춰서 크롤링하기 쉽게 만들기.

    return browser


def get_data(start, end, url):
    date_range = []
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    driver = load_chrome_browser()

    for date in date_generated:
        date_range.append(date.strftime("%Y%m%d"))

    title = []
    heart = []
    link_ = []
    content = []

    for i in date_range:
        driver.get(url + i)

        a = driver.page_source

        soup = BeautifulSoup(a, 'html.parser')

        for tag in soup.select('dt > a > span'):
            title.append(tag.text)

        for names in soup.select('div > em'):
            heart.append(names.text)

        for tags in soup.select('div > dt > a'):
            link_.append(tags['href'])

        link2_ = '[]'.join(link_)
        link2_ = link2_.replace('https:', '')
        link3_ = link2_.split('[]')

        for i in link3_:
            base = requests.get('https:' + i)
            base.encoding = 'utf-8'
            soup = BeautifulSoup(base.text, 'html.parser', from_encoding='utf-8')

            for contents in soup.find_all('div', class_='par'):
                content.append(contents.text)

    return title, heart, link_, content