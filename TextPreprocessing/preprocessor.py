import os

from konlpy.tag import Okt, Kkma, Mecab, Hannanum
from multiprocessing import Pool
from functools import partial

import re


class TextPreProcessor(object):

    @staticmethod
    def __get_stop_words():
        """ 한국어 불용어 리스트 가져오기.

        영어는 nltk안에 내장된 불용어 리스트가 있지만
        한국어의 경우 없기 때문에 자료를 다운 받아 사용.
        Reference - https://bab2min.tistory.com/544
        :return: stop words
        """
        stop_words = []

        with open('/Users/hongnadan/PycharmProjects/Generate-HeadLine/TextPreprocessing/한국어불용어100.txt', 'r', encoding='utf-8-sig') as f:
            while True:
                a = f.readline()
                if a:
                    a = a.split()[0]
                    stop_words.append(a)
                else:
                    break
        return stop_words

    @staticmethod
    def __select_tokenize(method: str):
        # default tokenizer is okt
        tokenizer = Okt()

        if method.lower() == "okt":
            tokenizer = Okt()
        elif method.lower() == "kkma":
            tokenizer = Kkma()
        elif method.lower() == "mecab":
            tokenizer = Mecab()
        elif method.lower() == "hannanum":
            tokenizer = Hannanum()
        else:
            print("you don't input correct tokenizer method so set-up default tokenizer okt")

        return tokenizer

    @staticmethod
    def text_to_wordlist(text: str, tokenizer, remove_stopwords=False, pos_presence=True) -> list:
        """ 텍스트 데이터 전처리 함수.

        :param review: input review or text data.
        :param remove_stopwords: whether remove stopwords
        :return:
        """
        # 1. 특수문자를 공백으로 바꿔줌
        text = re.sub("[^가-힣-ㄱ-ㅎㅏ-ㅣ\\s]", " ", text)
        text = TextPreProcessor.remove_emoji(text)

        tokenizer = TextPreProcessor.__select_tokenize(tokenizer)

        if tokenizer == "okt":
            if pos_presence:
                words = tokenizer.pos(text, stem=True)
            else:
                words = tokenizer.morphs(text, stem=True)
        else:
            if pos_presence:
                words = tokenizer.pos(text)
            else:
                words = tokenizer.morphs(text)

        # 2. 불용어 목록 가져오기
        stop_words = TextPreProcessor.__get_stop_words()

        # 3. 불용어 제거
        if remove_stopwords:
            words = [w for w in words if w not in stop_words]

        # 4. 리스트 형태로 반환
        return words

    @staticmethod
    def text_to_pos_words(text: str, tokenizer, remove_stopwords=False) -> list:
        """

        :param text: 텍스트 데이터
        :param remove_stopwords: 불용어 처리 여부.
        :return: 전처리된 텍스트 데이터
        """
        # 1. 특수문자를 공백으로 바꿔줌
        text = re.sub("[^가-힣-ㄱ-ㅎㅏ-ㅣ\\s]", " ", text)

        # 2. 어간추출 (konlpy tokenize 사용)
        tokenizer = TextPreProcessor.__select_tokenize(tokenizer)

        words = tokenizer.pos(text, stem=True, norm=True)

        # 3. 불용어 목록 가져오기
        stop_words = TextPreProcessor.__get_stop_words()

        # 4. 불용어 제거
        if remove_stopwords:
            words = [w for w in words if not w in stop_words]

        # 5. 동사, 명사만 추출.
        result = []
        for w in words:
            if w[1] in ["Noun", "Verb"]:
                result.append(w[0])

        return result

    @staticmethod
    def text_to_join_words(text: str, remove_stopwords=False) -> str:
        """ word 단위로 토큰화 된 text 데이터를 합쳐주는 함수.

        :param text: input review or text data.
        :return: Tokenized sentences
        """
        words = TextPreProcessor.review_to_wordlist(\
            text, remove_stopwords=False)
        join_words = ' '.join(words)
        return join_words

    @staticmethod
    def text_to_sentences(text: str, tokenizer, remove_stopwords=False) -> list:
        """ 불용어 및 전처리 된 문장 데이터를 만들어 주는 함수.

        :param text: input review or text data.
        :return: sentences
        """
        tokenizer = TextPreProcessor.__select_tokenize(tokenizer)

        # 1. konlpy okt을 사용해서 단어로 토큰화 하고 공백 등을 제거한다.
        raw_sentences = tokenizer.morphs(text.strip())

        # 2. 각 문장을 순회한다.
        sentences = []
        for raw_sentence in raw_sentences:
            # 비어있다면 skip
            if len(raw_sentence) > 0:
                # 태그제거, 알파벳문자가 아닌 것은 공백으로 치환, 불용어제거
                sentences.append(\
                    TextPreProcessor.review_to_wordlist(\
                    raw_sentence, remove_stopwords))
        return sentences

    @staticmethod
    def remove_emoji(text: str):
        """ Remove emoji data.

        :param df: dataframe
        :return: remove emoji
        """
        EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        return EMOJI.sub(r'', text)

    @staticmethod
    def apply_by_multiprocessing(data: list, func, **kwargs) -> list:
        # 키워드 파라메터를 꺼냄

        pool = Pool(processes=os.cpu_count())

        if "tokenizer" in kwargs.keys():
            tokenizer = kwargs.pop("tokenizer")
            func = partial(func, tokenizer=tokenizer)
        if "stopwords" in kwargs.keys():
            stopwords = kwargs.pop("stopwords")
            func = partial(func, remove_stopwords=stopwords)
        if "pos_presence" in kwargs.keys():
            pos_presence = kwargs.pop("pos_presence")
            func = partial(func, pos_presence=pos_presence)

        result = pool.map(func, data)
        pool.close()
        pool.join()

        return result