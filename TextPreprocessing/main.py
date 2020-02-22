from DataHandler.MysqlHandler import MysqlHandler
from DataHandler.utils import get_clean_df, handle_pickle, save_data
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


def get_summarizes(conf=None):
    sql = f"select {conf['title_column']}, {conf['content_column']} from {conf['table']}"
    handler = MysqlHandler(host=conf['db_host'], user=conf['db_user'],
                           password=conf['db_passwd'], port=int(conf['db_port']))

    df = get_clean_df(sql, handler)
    data = [list(df[col]) for col in df]
    save_data(data, '{}.pkl'.format(conf['table']))


def clean_summarizes(conf=None):
    path = '{}.pkl'.format(conf['table'])
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
    config = ConfigHandler.loadFromFile()
    get_summarizes(config)
    clean_summarizes(config)
    return None


if __name__ == '__main__':
    main()
