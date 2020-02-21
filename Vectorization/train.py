from gensim.models import Word2Vec
from TextPreprocessing.MysqlHandler import MysqlHandler
from utils import get_data, get_corpus
from Vectorizer import train_word2vec, transfer_word2vec
from Vectorizer import load_model, train_n_gram, train_tfidf


def train(data, method="word2vec", n=None, transfer=False, save=False, path=None):
    """ Train Vectorizing Model by using collected data.

    Trained Vectorization Reference - https://github.com/Kyubyong/wordvectors
    :param data: input data for train.
    :param method: Vectorizer Method (word2vec, TF-IDF, n-gram)
    :param n: select counts for n-gram model.
    :param transfer: transfer learning existence.
    :param save: save existence.
    :param path: save path.
    :return: transfer trained model.
    """
    total_corpus = []

    for d in data:
        total_corpus += get_corpus(d)

    if method == "tfidf":
        trained_model = train_tfidf(data)
    elif method == "ngram":
        if n is not None:
            trained_model = train_n_gram(data, n)
        else:
            trained_model = train_n_gram(data, 2)
    else:
        if transfer:
            trained_model = load_model(path)
            trained_model = transfer_word2vec(trained_model, total_corpus)
        else:
            trained_model = train_word2vec(total_corpus)

    if save:
        if path is not None:
            trained_model.save(path)
        else:
            trained_model.save("Vectorizer.model")

    return trained_model


if __name__ == "__main__":
    HOST = ""
    USER = ""
    PASSWORD = ""
    PORT = 0

    handler = MysqlHandler(host=HOST, user=USER,
                           password=PASSWORD, port=PORT)

    sql = ""
    data = get_data(sql, handler)
    method = ""
    train(data, method=method)