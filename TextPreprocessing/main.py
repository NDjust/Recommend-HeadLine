from DataHandler.MysqlHandler import MysqlHandler
from DataHandler.utils import get_clean_df, handle_pickle, save_title_summarizes_pair, save_summarizes
from TextPreprocessing.preprocessor import TextPreProcessor
import numpy as np
from DataHandler import ConfigHandler

def fit_processor(data, func, **kwargs) -> list:
    # convert data type
    data = list(np.asarray(data))
    print("Cleansing Text data")

    # preprocessing by us multiprocessing
    data = TextPreProcessor.apply_by_multiprocessing(
        data=data, func=func, tokenizer=kwargs.pop('tokenizer'),
        stopwords=kwargs.pop("stopwords")
    )

    return data


def get_title_summarizes_pair():
    conf = ConfigHandler.loadFromFile()
    sql = f"select {conf['title_column']}, {conf['content_column']} from {conf['title_table']}"
    handler = MysqlHandler(host=conf['db_host'], user=conf['db_user'],
                           password=conf['db_passwd'], port=int(conf['db_port']))

    df = get_clean_df(sql, handler)
    data = [list(df[col]) for col in df]
    save_title_summarizes_pair(data, '{}.pkl'.format(conf['title_table']))


def get_titles():
    conf = ConfigHandler.loadFromFile()
    sql = f"select {conf['title_column']} from {conf['title_table']}"
    handler = MysqlHandler(host=conf['db_host'], user=conf['db_user'],
                           password=conf['db_passwd'], port=int(conf['db_port']))
    df = get_clean_df(sql, handler)
    data = []
    for col in df:
        for title in df[col]:
            data.append(title)
    handle_pickle(f"title_{conf['title_table']}.pkl", data=data, is_save=True)


def get_summarizes():
    conf = ConfigHandler.loadFromFile()
    sql = f"select {conf['content_column']} from {conf['content_table']}"
    handler = MysqlHandler(host=conf['db_host'], user=conf['db_user'],
                           password=conf['db_passwd'], port=int(conf['db_port']))
    df = get_clean_df(sql, handler)
    data = []
    for col in df:
        for content in df[col]:
            data.append(content)

    save_summarizes(data, 'content_{}.pkl'.format(conf['content_table']))


def clean_summarizes():
    conf = ConfigHandler.loadFromFile()
    title_path = 'title_{}.pkl'.format(conf['title_table'])
    content_path = 'content_{}.pkl'.format(conf['content_table'])
    titles = handle_pickle(title_path)
    contents = handle_pickle(content_path)

    none_remove = []
    for content in contents:
        if content != None:
            none_remove.append(content)

    max_len = max([len(title) for title in titles])
    news = []
    for row in range(len(none_remove)):
        cur_sums = none_remove[row]
        new_sums = [[], []]
        for i in range(len(cur_sums[0])):
            if cur_sums[0][i].strip() != '' and len(cur_sums[0][i]) < max_len:
                new_sums[0].append(cur_sums[0][i])
                new_sums[1].append(cur_sums[1][i])
            if len(new_sums[0]) > 2:
                news.append(new_sums)

    handle_pickle('clean_' + content_path, data=news, is_save=True)


def clean_title_summarizes_pair():
    conf = ConfigHandler.loadFromFile()
    path = '{}.pkl'.format(conf['title_table'])
    data = handle_pickle(path)

    none_remove = []
    for row in range(len(data)):
        if data[row] != None:
            none_remove.append(data[row])

    max_len = 0
    for row in range(len(none_remove)):
        if len(none_remove[row][0]) > max_len:
            max_len = len(none_remove[row][0])

        cur_sums = none_remove[row][2]
        new_sums = [[], []]
        for i in range(len(cur_sums[0])):
            if cur_sums[0][i] != '':
                new_sums[0].append(cur_sums[0][i])
                new_sums[1].append(cur_sums[1][i])
        none_remove[row][2] = new_sums

    news = []
    for row in range(len(none_remove)):
        cur_sums = none_remove[row][2]
        new_sums = [[], []]
        for i in range(len(cur_sums[0])):
            if len(cur_sums[0][i]) < max_len:
                new_sums[0].append(cur_sums[0][i])
                new_sums[1].append(cur_sums[1][i])
        if len(new_sums[0]) > 2:
            none_remove[row][2] = new_sums
            news.append(none_remove[row])

    handle_pickle('clean_' + path, data=news, is_save=True)


def main():
    get_title_summarizes_pair()
    clean_title_summarizes_pair()
    return None


if __name__ == '__main__':
    main()
