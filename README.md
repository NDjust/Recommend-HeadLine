# Headline Recommend (KPMG)
[![license](https://img.shields.io/badge/License-AGPL-red)](https://github.com/NDjust/Generate-HeadLine/blob/master/LICENSE)
[![code](https://img.shields.io/badge/Code-Python3.7-blue)](https://docs.python.org/3/license.html)
[![data](https://img.shields.io/badge/Data-news-blueviolet)](https://news.chosun.com/ranking/list.html)
[![member](https://img.shields.io/badge/Project-Member-brightgreen)]()
> Text-mining을 통해 Content에 대한 Headline을 추천해주는 프로젝트

## 📖 Introduction  
글을 작성하는 사람은 Headline을 만들 때, 다른 사람의 이목을 끄는 Headline을 선정하거나  
정보 전달이 명확한 Headline을 선정하는 등 글의 취지에 맞게 Headline을 선정하게 됩니다.  
  
'첫 문장은 제목이다'라는 말처럼 Headline을 잘 만드는 것이 중요해지고 있습니다.  
  
우리는 Headline을 작성하는 사람들의 부담을 덜어주고자 해당 프로젝트를 진행하게 되었습니다.  
  
## Participation Member
- 홍나단 : 010-6681-8139  
- 박성아 : 010-5619-9295  
- 박규훤 : 010-6473-4049  
- 한예찬 : 010-9042-1834  

## Role
- Data Engineering : 홍나단, 박규훤  
- Data Analysis : 박성아, 한예찬  
- Modeling : All  

## 📂 Directory structure
``` 
  |-Analysis           
  |  |-DataJoin.ipynb                   # 분리된 데이터 통합 코드
  |  |-KewordSim.ipynb                  # 제목과 본문간의 단어 유사도 측정 코드
  |  |-NounExtrac.ipynb                 # 명사 추출 코드
  |  |-SentSimPre.ipynb                 # 문장 유사도 전처리 코드
  |  |-TextRank.ipynb                   # TextRank를 이용한 키워드 추출 코드
  |
  |-Comparing
  |  |-ExtractTitle.py                  # 유사도 비교 후 문장 추천해주는 코드
  |  |-Similarity.py                    # Cosine 유사도 구해주는 코드
  |
  |-Crawler 
  |  |-Crawling.py                      # 조선일보 크롤링 해주는 코드
  |  |-CrawlingTester.py                # 크롤링 테스트 코드                         
  |  |-TestDBconnector.py               # DB 연결 테스트 코드
  |  |-main.py                          # 크롤링 실행 코드
  |  |-saver.py                         # DB or CSV로 저장해주는 코드
  |
  |-DataHandler
  |  |-MysqlHandler.py                  # Mysql에서 데이터를 가져오는 코드
  |  |-utils.py                         # 데이터 처리하는 코드
  |
  |-TextPreprocessing 
  |  |-TextSummarizer.py                # 문장요약해주는 코드
  |  |-preprocessing.py                 # 토큰화, 품사 태깅 해주는 코드
  |  |-main.py                          # 전처리 실행 해주는 코드
  |  |-stopword.txt                     # 불용어 목록
  |  |-한국어불용어100.txt               # 한국어 불용어 목록
  |
  |-Vectorization
  |  |-Vectorizer.py                    # 벡터화 모델 세팅하는 코드
  |  |-train.py                         # 모델 학습시키는 코드
  |
  |-.gitignore                               
  |
  |-LICENSE                              
  |
  |-README.md                           # 해당 문서
  |
  |-requirements.txt                    # 사전 설치 목록
  |
  |-run.py                              # 프로젝트를 실행해주는 파일
```

## 💻 System requirements
- beautifulsoup4==4.6.0
- gensim==3.8.0
- jpype1==0.7.1
- konlpy==0.5.2
- numpy==1.18.1
- pandas==0.25.3
- pymysql==0.9.3
- requests==2.22.0
- scikit-learn==0.22.1
- selenium==3.141.0
- textdistance==4.1.3
- tqdm==4.42.1






