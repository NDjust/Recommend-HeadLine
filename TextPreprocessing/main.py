from DataHandler.MysqlHandler import MysqlHandler
from DataHandler.utils import get_clean_df, handle_pickle
from TextPreprocessing.preprocessor import TextPreProcessor
import numpy as np

HOST = ""
USER = ""
PASSWORD = ""
PORT = 0

DB_TABLE_1 = ""
DB_TABLE_2 = ""


def fit_processor(data, func, **kwargs) -> list:
    # convert data type
    data = list(np.asarray(data))
    print("Cleansing Text data")

    # preprocessing by us multiprocessing
    data = TextPreProcessor.apply_by_multiprocessing(
        data=data, func=func, tokenizer=kwargs.pop('tokenizer'),
        stopwords=kwargs.pop("stopwords"), workers=kwargs.pop("workers")
    )

    return data


def main():
    date = [[20150101, 20160101], [20160101, 20170101], [20170101, 20180101], [20180101, 20190101],
            [20190101, 20200101]]
    for start, end in date:
        sql = f"select title, content from {DB_TABLE_2} " \
              f"where created_date >= {start} and created_date < {end}"
        handler = MysqlHandler(host=HOST, user=USER,
                               password=PASSWORD, port=PORT)

        df = get_clean_df(sql, handler)

        clean_title = fit_processor(df["title"], func=TextPreProcessor.text_to_wordlist,
                                    workers=4, tokenizer="mecab", stopwords=True)
        clean_content = fit_processor(df["content"], func=TextPreProcessor.text_to_wordlist,
                                      workers=4, tokenizer="mecab", stopwords=True)
        data = [[clean_title[i], clean_content[i]] for i in range(len(clean_content))]

        SAVE_PATH = "./data/" + DB_TABLE_2 + str(start) + ".pickle"
        handle_pickle(data=data, file_name_path=SAVE_PATH, is_save=True)

    return None


if __name__ == '__main__':
    main()