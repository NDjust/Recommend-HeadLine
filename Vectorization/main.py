from TextPreprocessing.MysqlHandler import MysqlHandler
from TextSummarizer import TextRank
from multiprocessing import Pool
from utils import add_summary_sentence, apply_by_multiprocessor, get_data
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
    """ Make dictionary.

    :param handler: MySql Handler
    :param sql: sql query
    :param save: save existence.
    :param path: save path
    :return: data word dictionary
    """
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


def save_data(path=None) -> list:
    """ Save title, content, summary sentences data.

    :param path: save path
    :return: [title, content, summary_sentences] data
    """
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
        result = apply_by_multiprocessor(data=data, func=add_summary_sentence, workers=4)

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