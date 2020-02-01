from Crawling import *
from saver import *

import datetime


URL = "http://news.chosun.com/ranking/list.html?type=&site=www&scode=star&term=&date="
START = datetime.datetime.strptime("20190101", "%Y%m%d")
END = datetime.datetime.strptime("20190201", "%Y%m%d")


def main():
    date_range = []
    date_generated = [START + datetime.timedelta(days=x)
                      for x in range(0, (END - START).days)]

    for date in date_generated:
        date_range.append(date.strftime("%Y%m%d"))

    for i in date_range:
        url = URL + i
        title, views, article_link, content = get_data(url)
        save_csv(title, views, article_link,
                 content, "chosun_news_to_19_01_from_19_03")

    return


if __name__ == '__main__':
    main()