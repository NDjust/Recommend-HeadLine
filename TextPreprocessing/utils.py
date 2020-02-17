from multiprocessing import Pool
from preprocessor import TextPreProcessor
from MysqlHandler import MysqlHandler

import pandas as pd
import numpy as np
import pickle


def get_clean_df(sql: str, handler: MysqlHandler) -> pd.DataFrame:
    with handler:
        print("Load data in mysql")
        df = handler.mysql_to_df(sql)

    if df is None:
        return None

    df = df.dropna()

    return df


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


def apply_by_multiprocessor(data, func, **kwargs):
    print("Start Multiprocessing")
    workers = kwargs.pop("workers")
    pool = Pool(processes=workers)
    result = pool.map(data, func)

    return result


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