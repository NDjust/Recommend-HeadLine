from konlpy.tag import Okt
from multiprocessing import Pool

import re
import pandas as pd
import numpy as np


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

        with open('./한국어불용어100.txt', 'r', encoding='utf-8-sig') as f:
            while True:
                a = f.readline()
                if a:
                    a = a.split()[0]
                    stop_words.append(a)
                else:
                    break
        return stop_words

    @staticmethod
    def review_to_wordlist(text: str, remove_stopwords=False, pos_presence=True) -> list:
        """ 텍스트 데이터 전처리 함수.

        :param review: input review or text data.
        :param remove_stopwords: whether remove stopwords
        :return:
        """
        # 1. 특수문자를 공백으로 바꿔줌
        review_text = re.sub("[^가-힣-ㄱ-ㅎㅏ-ㅣ\\s]", " ", text)

        # 3. 어간추출 (konlpy okt tokenize 사용)
        okt = Okt()
        if pos_presence:
            words = okt.pos(text, stem=True)
        else:
            words = okt.morphs(review_text, stem=True)

        # 4. 불용어 목록 가져오기
        stop_words = TextPreProcessor.__get_stop_words()

        # 5. 불용어 제거
        if remove_stopwords:
            words = [w for w in words if not w in stop_words]

        # 6. 리스트 형태로 반환
        return words

    @staticmethod
    def review_to_pos_words(text: str, remove_stopwords=False) -> list:
        """

        :param text: 텍스트 데이터
        :param remove_stopwords: 불용어 처리 여부.
        :return: 전처리된 텍스트 데이터
        """
        # 1. 특수문자를 공백으로 바꿔줌
        text = re.sub("[^가-힣-ㄱ-ㅎㅏ-ㅣ\\s]", " ", text)

        # 3. 어간추출 (konlpy okt tokenize 사용)
        okt = Okt()
        words = okt.pos(text, stem=True, norm=True)

        # 4. 불용어 목록 가져오기
        stop_words = TextPreProcessor.__get_stop_words()

        # 5. 불용어 제거
        if remove_stopwords:
            words = [w for w in words if not w in stop_words]

        # 6. 동사, 명사만 추출.
        result = []
        for w in words:
            if w[1] in ["Noun", "Verb"]:
                result.append(w[0])

        return result

    @staticmethod
    def review_to_join_words(text: str, remove_stopwords=False) -> str:
        """ word 단위로 토큰화 된 text 데이터를 합쳐주는 함수.

        :param text: input review or text data.
        :return: Tokenized sentences
        """
        words = TextPreProcessor.review_to_wordlist(\
            text, remove_stopwords=False)
        join_words = ' '.join(words)
        return join_words

    @staticmethod
    def review_to_sentences(text: str, remove_stopwords=False) -> list:
        """ 불용어 및 전처리 된 문장 데이터를 만들어 주는 함수.

        :param text: input review or text data.
        :return: sentences
        """
        okt = Okt()

        # 1. konlpy okt을 사용해서 단어로 토큰화 하고 공백 등을 제거한다.
        raw_sentences = okt.morphs(text.strip())

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
        # 키워드 항목 중 workers 파라메터를 꺼냄
        workers = kwargs.pop('workers')
        # 위에서 가져온 workers 수로 프로세스 풀을 정의
        pool = Pool(processes=workers)
        # 실행할 함수와 데이터프레임을 워커의 수 만큼 나눠 작업
        result = pool.map(func, data)
        pool.close()
        # 작업 결과를 합쳐서 반환
        return result