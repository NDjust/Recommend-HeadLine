from Crawling import *
from saver import *

import datetime


URL = "http://news.chosun.com/ranking/list.html?type=&site=www&scode=star&term=&date="
START = datetime.datetime.strptime("20190201", "%Y%m%d")
END = datetime.datetime.strptime("20190301", "%Y%m%d")
TABLE_NAME = "chosun_news"


def main(save_method):
    date_range = []
    date_generated = [START + datetime.timedelta(days=x)
                      for x in range(0, (END - START).days)]

    for date in date_generated:
        date_range.append(date.strftime("%Y%m%d"))

    for date in date_range:
        url = URL + date
        title, views, article_link, content = get_data(url)
        if save_method == "csv":
            print("Saver Type CSV")
            save_csv(title, views, article_link, content, date, "chosun_news_to_19_01_from_19_03")
        elif save_method == "db":
            print("Saver Type db in mysql")
            save_db(TABLE_NAME, title, date, views, article_link, content)

    return


if __name__ == '__main__':
    print("Select saver type(csv or db): ")
    save_type = input()
    main(save_type)