from TextPreprocessing.preprocessor import TextPreProcessor
from gensim.models import Word2Vec
from TextPreprocessing.MysqlHandler import MysqlHandler
from utils import get_data


HOST = ""
USER = ""
PASSWORD = ""
PORT = 0

DB_TABLE_1 = ""
DB_TABLE_2 = ""

date = []
data_handler = MysqlHandler(host=HOST, user=USER,
                            password=PASSWORD, port=PORT)

trained_model = Word2Vec.load("path")


def train_data(save=False, path=None):

    for start, end in date:
        print(f"Start {start} date")
        field = "title"
        sql = f"select {field} from {DB_TABLE_1} " \
              f"where created_date >= {start} and created_date < {end}"

        data = get_data(sql=sql)

        print("Title data PreProcessing")
        data = TextPreProcessor.apply_by_multiprocessing(
            func=TextPreProcessor.text_to_wordlist, data=data,
            workers=4, stopwords=True, tokenizer="okt"
        )
        print(data)

        print("Word2Vec Build vocab by using Title data ")
        result = trained_model.build_vocab(data, update=True)

        print("Word2Vec train by using Title data ")
        result = trained_model.train(data,
                                     total_examples=trained_model.corpus_count,
                                     epochs=trained_model.epochs)
        print("Complete title data train")
        print(result)
        print(trained_model)

        field = "content"
        sql = f"select {field} from {DB_TABLE_1} " \
              f"where created_date >= {start} and created_date < {end}"

        data = get_data(sql=sql)

        print("content data PreProcessing")
        data = TextPreProcessor.apply_by_multiprocessing(
            func=TextPreProcessor.text_to_wordlist, data=data,
            workers=4, stopwords=True, tokenizer="okt"
        )

        print("Word2Vec Build vocab by using content data ")
        result = trained_model.build_vocab(data, update=True)

        print("Word2Vec train by using content data ")
        result = trained_model.train(data,
                                     total_examples=trained_model.corpus_count,
                                     epochs=trained_model.epochs)

        print("Complete content data train")
        print(result)
        print(trained_model)

    if save:
        trained_model.save(path)

    return trained_model


if __name__ == "__main__":
    path = ""
    model = train_data(save=True, path=path)
