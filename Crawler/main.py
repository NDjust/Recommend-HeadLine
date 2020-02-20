from Crawling import *
from saver import *

import datetime


URL = "https://news.chosun.com/ranking/list.html?type=&site=www&scode=editorials&term=&date="
START = datetime.datetime.strptime("20191101", "%Y%m%d")
END = datetime.datetime.strptime("20200201", "%Y%m%d")
TABLE_NAME = ""


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
            save_csv(title=title, date=date, views=views,
                     article_link=article_link, content=content,
                     file_name=f"{TABLE_NAME}_to_{START}_from_{END}")

        elif save_method == "db":
            print("Saver Type db in mysql")
            save_db(table_name=TABLE_NAME, title=title,
                    date=date, views=views,
                    article_link=article_link, content=content)

    return


if __name__ == '__main__':
    print("Select saver type(csv or db): ")
    save_type = input()
    main(save_type)