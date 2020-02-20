from pymysql import Error

import pymysql
import os
import csv
import pandas as pd


def create_table(sql):

    try:
        conn = pymysql.connect(host="", user="",
                               password="",
                               charset="utf8")
        print(conn.get_server_info())

        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Error as e:
        print(e)

    return


def save_db(table_name, title, date, views, article_link, content):
    try:
        conn = pymysql.connect(host="", user="",
                               password="",
                               charset="utf8", port=None)
        print(conn.get_server_info())

        cursor = conn.cursor()

        print("\nSave data in DB")

        for i in range(len(title)):
            sql = "insert into {} values(" \
                  "%s, %s, %s, %s, %s)".format(table_name)

            cursor.execute(sql, (title[i], date, views[i], article_link[i], content[i]))
            conn.commit()

        conn.close()

    except Error as e:
        print(e)


def save_csv(title, date, views, article_link, content, file_name):
    data = []

    for i in range(len(title)):
        data.append([title[i], date, views[i], article_link[i], content[i]])

    print(data)

    if "data" not in os.listdir("./"):
        os.mkdir("./data")

    if (file_name + ".csv") not in os.listdir("./data/"):
        print("=========Generate CSV File==============")
        df = pd.DataFrame(data, columns=["title", "date", "views", "article_link", "content"])
        df.to_csv(f'./data/{file_name}.csv', encoding="utf-8-sig", index=False)
    else:
        with open(f"./data/{file_name}.csv", "a", encoding="utf-8") as f:
            print("========Add data in CSV File===========")
            writer = csv.writer(f)
            writer.writerows(data)

    return

