from .MysqlHandler import MysqlHandler
from .utils import get_clean_df, handle_pickle, fit_processor
from .utils import apply_by_multiprocessor
from .preprocessor import TextPreProcessor

HOST = ""
USER = ""
PASSWORD = ""
PORT = 0
sql = 0
DB_TABLE = ""

date = []
SAVE_PATH = ""


def main():
    for start, end in date:
        sql = f"select title, content from {DB_TABLE} " \
              f"where created_date >= {start} created_date < {end}"
        handler = MysqlHandler(host=HOST, user=USER,
                               password=PASSWORD, port=PORT)
        df = get_clean_df(sql, handler)
        clean_title = fit_processor(df["title"], fun=TextPreProcessor.review_to_wordlist,
                                    workers=4)

        clean_content = fit_processor(df["content"], func=TextPreProcessor.review_to_wordlist,
                                      workers=4)

        data = [[clean_title[i], clean_content[i]] for i in range(len(clean_content))]

        handle_pickle(data, SAVE_PATH, is_save=True)

    return None


if __name__ == '__main__':
    main()