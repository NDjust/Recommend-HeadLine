from multiprocessing import Pool
from functools import partial
from TextPreprocessing.TextSummarizer import TextRank
from TextPreprocessing.preprocessor import TextPreProcessor

from DataHandler.MysqlHandler import MysqlHandler

import pandas as pd
import re
import pickle


def get_clean_df(sql: str, handler: MysqlHandler) -> pd.DataFrame:
    with handler:
        print("Load data in mysql")
        df = handler.mysql_to_df(sql)

    if df is None:
        return None

    df = df.dropna()

    return df


def handle_pickle(file_name_path, data=None, is_save=False):
    if is_save:
        print("Save Data to Pickle")
        with open(file_name_path, mode="wb") as f:
            pickle.dump(data, f)

        return None
    else:
        with open(file_name_path, mode="rb") as f:
            data = pickle.load(f)

        return data


def save_data(data: list, path=None) -> list:
    """ Save title, content, summary sentences data.

    :param data: input data (title, content)
    :param path: save path
    :return: [title, content, summary_sentences] data
    """

    title = data[0]
    content = data[1]

    data = [[title[i], content[i]] for i in range(len(data)) if i != 6140]
    result = apply_by_multiprocessor(data=data, func=add_summary_sentence, workers=4)

    with open(path, mode="wb") as f:
        pickle.dump(result, f)

    return result


def add_summary_sentence(data) -> list:
    """ add summary data.

    :param data: [title, content] list data
    :return: [title, content, summary_sentences] list data
    """
    title = data[0]
    content = data[1]
    content = re.sub('["\'“”‘’◆▲★●■◀▼▶]', '', content)

    # except Wrong value contents.
    try:
        sum = TextRank(content).summarize(5)
    except:
        return None

    return [title, content, sum]


def get_data(data_handler, sql):
    """ Get data about the sql query.

    :param data_handler: sql handler
    :param sql: sql query
    :return: data(about the sql query).
    """
    with data_handler:
        data = data_handler.get_data(sql=sql)

    try:
        data = data
    except:
        return None

    return data


def get_corpus(data: list) -> list:
    print("Convert data to corpus data")

    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt",
        pos_presence=False
    )

    return data


def apply_by_multiprocessor(data, func, **kwargs):
    print("Start Multiprocessing")

    if "dic" in kwargs.keys():
        dic = kwargs.pop("dic")
        func = partial(func, dic=dic)

    workers = kwargs.pop("workers")
    pool = Pool(processes=workers)
    result = pool.map(func, data)
    pool.close()
    pool.join()

    return result


def make_dict(data, save=False, path=None):
    """ Make dictionary.

    :param data : input data.
    :param save: save existence.
    :param path: save path
    :return: data word dictionary
    """
    dic = dict()

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