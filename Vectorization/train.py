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


def load_model(path):
    model = Word2Vec.load(path)

    return model


def get_corpus(data) -> list:
    print("Convert data to corpus data")

    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt"
    )

    return data


def train_word2vec(data):
    model = Word2Vec(sentences=data,
                     size=100, window=5,
                     min_count=1, workers=4)

    return model


def transfer_word2vec(trained_model, corpus):
    # Update Vocab
    trained_model.build_vocab(corpus, update=True)

    print("Word2Vec train by using Title data ")
    result = trained_model.train(corpus,
                                 total_examples=trained_model.corpus_count,
                                 epochs=trained_model.epochs)
    print("Complete train")
    return result


def train_data(sql, transfer=False, save=False, path=None):
    """ Word2Vec transfer learning by using collected data.

    Trained Vectorizing Reference - https://github.com/Kyubyong/wordvectors
    :param save: save existence.
    :param path: save path.
    :return: transfer trained model.
    """

    data = get_data(sql)
    total_corpus = []

    for d in data:
        total_corpus += get_corpus(d)

    if transfer:
        trained_model = load_model(path)
        trained_model = transfer_word2vec(trained_model, total_corpus)
    else:
        trained_model = train_word2vec(total_corpus)

    if save:
        trained_model.save(path)

    return trained_model



if __name__ == "__main__":
    pass