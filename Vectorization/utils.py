from multiprocessing import Pool
from functools import partial
from TextSummarizer import TextRank
from TextPreprocessing.preprocessor import TextPreProcessor

import re
import pickle


def clean_text(data):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('["\'“”‘’◆▲★●■◀▼▶]', '', data)

    return text


def add_summary_sentence(data) -> list:
    """ add summary data.

    :param data: [title, content] list data
    :return: [title, content, summary_sentences] list data
    """
    title = data[0]
    content = data[1]
    content = clean_text(content)

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


def get_corpus(data) -> list:
    print("Convert data to corpus data")

    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt"
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

    :param handler: MySql Handler
    :param sql: sql query
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