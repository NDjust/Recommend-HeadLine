from multiprocessing import Pool
from functools import partial
from TextSummarizer import TextRank

import re


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


if __name__ == '__main__':
    from TextPreprocessing.MysqlHandler import MysqlHandler
    from pprint import pprint
    handler = MysqlHandler(host="svclaw.ipdisk.co.kr",
                           user="skeks463", password="skeks463",
                           port=8005)
    sql = "select * from kpng.enter_news " \
          "where created_date = 20190101"

    pprint(get_data(handler, sql))
    pprint(len(get_data(handler, sql)[0]))