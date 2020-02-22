from DataHandler.MysqlHandler import MysqlHandler
from DataHandler.utils import get_clean_df, handle_pickle, save_data
from TextPreprocessing.preprocessor import TextPreProcessor
import numpy as np

HOST = ""
USER = ""
PASSWORD = ""
PORT = 0

DB_TABLE_1 = ""
DB_TABLE_2 = ""

DATA_PATH = 'summarizes.pkl'


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


def get_summarizes(save_path='untitled.pkl'):
    date = [[20190801, 20200201]]

    for start, end in date:
        sql = f"select title, content from {DB_TABLE_2} " \
              f"where created_date >= {start} and created_date < {end}"
        handler = MysqlHandler(host=HOST, user=USER,
                               password=PASSWORD, port=PORT)

        df = get_clean_df(sql, handler)

        data = [list(df[col]) for col in df]

        save_data(data, save_path)


def clean_summarizes(path='untitled.pkl'):
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


def main(path):
    get_summarizes(path)
    clean_summarizes(path)
    return None


if __name__ == '__main__':
    main(DATA_PATH)
