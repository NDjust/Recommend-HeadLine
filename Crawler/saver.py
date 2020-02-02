from pymysql import Error

import pymysql
import os
import csv
import pandas as pd


def save_db(table_name, title, views, article_link, content):
    try:
        conn = pymysql.connect(host="", user="",
                               password="", db="",
                               charset="")
        print(conn.get_server_info())

        cursor = conn.cursor()

        print("\nSave data in DB")

        for i in range(len(title)):
            sql = f"insert into {table_name} values(" \
                  f"{title[i]}, {views[i]}, {article_link[i]}, {content[i]})"

        cursor.execute(sql)
        conn.commit()

        conn.close()

    except Error as e:
        print(e)


def save_csv(title, views, article_link, content, file_name):
    data = []

    for i in range(len(title)):
        data.append([title[i], views[i], article_link[i], content[i]])
    print(data)
    if "data" not in os.listdir("./"):
        os.mkdir("./data")

    if (file_name + ".csv") not in os.listdir("./data/"):
        print("=========Generate CSV File==============")
        df = pd.DataFrame(data, columns=["title", "views", "article_link", "content"])
        df.to_csv(f'./data/{file_name}.csv', encoding="utf-8-sig", index=False)
    else:
        with open(f"./data/{file_name}.csv", "w") as f:
            print("========Add data in CSV File===========")
            writer = csv.writer(f, encoding="utf-8-sig")
            writer.writerows(data)

    return

