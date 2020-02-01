from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

PATH = "./webdriver/chromedriver"


def load_chrome_browser():
    """ Load chrome browser function.

    :return: Chrome browser Object.
    """
    chrome_options = Options()
    browser = webdriver.Chrome(
        "./webdriver/chromedriver", options=chrome_options)
    browser.set_window_size(1920, 1280) # 윈도우 사이즈를 맞춰서 크롤링하기 쉽게 만들기.

    return browser


def get_content(link):
    """ Get Article content.

        :param link: Article Url.
        :return: Article content.
        """
    driver = load_chrome_browser()
    body = ""

    try:
        driver.get(link)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        for content in soup.find_all("div", {"class": "par"}):
            body += content.text
    except WebDriverException as e:
        print(e)

    return body


def get_data(url):
    driver = load_chrome_browser()

    titles = []
    views = []
    article_link = []
    contents = []

    driver.get(url)
    a = driver.page_source

    soup = BeautifulSoup(a, 'html.parser')

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

