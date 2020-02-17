from TextPreprocessing.preprocessor import TextPreProcessor
from load import get_data
from gensim.models import Word2Vec

trained_model = Word2Vec.load("./trainedModel/ko/ko.bin")


def train_data():
    data = get_data("title")

    print("Title data PreProcessing")
    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt"
    )

    print("Word2Vec Build vocab by using Title data ")
    result = trained_model.build_vocab(data, update=True)

    print("Word2Vec train by using Title data ")
    result = trained_model.train(data,
                                 total_examples=trained_model.corpus_count,
                                 epochs=trained_model.epochs)
    print("Complete title data train")
    print(result)
    print(trained_model)

    print("content data PreProcessing")
    data = get_data("content")

    data = TextPreProcessor.apply_by_multiprocessing(
        func=TextPreProcessor.text_to_wordlist, data=data,
        workers=4, stopwords=True, tokenizer="okt"
    )
    print("Word2Vec Build vocab by using content data ")
    result = trained_model.build_vocab(data, update=True)

    print("Word2Vec train by using Title data ")
    result = trained_model.train(data,
                                 total_examples=trained_model.corpus_count,
                                 epochs=trained_model.epochs)

    print("Complete title data train")
    print(result)
    print(trained_model)
    return trained_model


if __name__ == "__main__":
    model = train_data()
    model.save("./trainedModel/transferW2V.model")
