from TextPreprocessing.MysqlHandler import MysqlHandler
from TextSummarizer import TextRank
from multiprocessing import Pool
from .utils import convert_data, apply_by_multiprocessor, get_data
from TextPreprocessing.preprocessor import TextPreProcessor

import numpy as np
import pickle

HOST = ""
USER = ""
PASSWORD = ""
PORT = 0

DB_TABLE_1 = ""
DB_TABLE_2 = ""
#
date = []


handler = MysqlHandler(host=HOST, user=USER,
                       password=PASSWORD, port=PORT)

target_table = ""


def make_dict(handler, sql, save=False, path=None):
    dic = dict()

    data = get_data(data_handler=handler, sql=sql)
    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt"
    )

    for li in data:
        for d in li:
            if d in dic.keys():
                dic[d] += 1
            else:
                dic[d] = 1

    if save:
        with open(path, mode="wb") as f:
            pickle.dump(dic, f)

    return dic


def save_data(path=None):
    for start, end in date:
        # get title
        sql = f"select title, content from {DB_TABLE_1} " \
              f"where created_date >= {start} and created_date < {end}"

        # get content
        df = get_data(sql)
        title = list(np.asarray(df["title"]))
        content = list(np.asarray(df["content"]))

        print(len(df["title"]))
        print(len(df["content"]))
        print(df.shape)

        data = [[title[i], content[i]] for i in range(df.shape[0]) if i != 6140]
        result = apply_by_multiprocessor(data=data, func=convert_data, workers=4)

        with open(path, mode="wb") as f:
            pickle.dump(result, f)

    return result


def main():
    dic_path = ""
    make_dict(handler, save=True, path=dic_path)
    data_path = ""
    save_data(data_path)


if __name__ == '__main__':
    main()