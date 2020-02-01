from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

PATH = "./webdriver/chromedriver"
URL = "http://news.chosun.com/ranking/list.html?type=&site=www&scode=star&term=&date="


def test_driver():
    chrome_options = Options()
    driver = webdriver.Chrome("./webdriver/chromedriver",
                              options=chrome_options)

    driver.set_window_size(1920, 1280)

    return driver


def test_get_content(url):
    """ Get Article content.

    :param url: Article Url.
    :return: Article content.
    """
    driver = test_driver()
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    body = ""

    for content in soup.find_all("div", {"class": "par"}):
        body += content.text

    return body


def test_get_data(url):
    """ Get chosun news top 30 article data.

    :param url: Chosun news top 30 link. (date choice)
    :return: news title, views ,link, content.
    """
    titles = []
    views = []
    article_link = []
    content = []

    driver = test_driver()
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    for title_tag in soup.select("dt > a > span"):
        titles.append(title_tag.text)

    for view_tag in soup.select("div > em"):
        views.append(view_tag.text)

    for link_tag in soup.select("div > dt > a"):
        # Convert href to link.
        link = "https:" + link_tag["href"]
        article_link.append(link)
        # Target article content.
        content.append(test_get_content(link))

    print(f"Top1 title {titles[0]}")
    print(f"Top1 views {views[0]}")
    print(f"Top1 Article line {article_link[0]}")
    print(f"Top1 content {content[0]}")

    return titles, views, article_link, content


def main():
    print("Get Chrome Browser")

    test_driver()

    print("Test Crawling title, views, link, content \n\n")

    test_get_data(URL)


if __name__ == "__main__":
    main()
