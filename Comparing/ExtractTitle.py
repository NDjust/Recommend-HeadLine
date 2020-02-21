from DataHandler.utils import apply_by_multiprocessor
from sklearn.feature_extraction.text import TfidfVectorizer
from Comparing.Similarity import cos_similarity
from Vectorization.train import train

import numpy as np
import pickle

file = 'news.pickle'


# Get summarized data and original title from article
def get_data(data_path):
    data = pickle.load(open(data_path, 'rb'))
        
    total_sum = []
    total_title = []
    
    for row in range(len(data)):
        if data[row] is None:
            continue

        if data[row][0] in total_title:
            continue
        total_title.append(data[row][0])
        total_sum.append(data[row][2])
        
    return total_title, total_sum


# Select title from summarizes
def extract_title(data):
    index = data[0]
    total_title = data[1]
    total_sum = data[2]
    print(index)
    
    summarizes = total_sum[index]
    title = total_title[index]
    similarity_simple = []
    similarity_index = []
    cur_total = total_title + summarizes
    
    cur_total = [cur_total[j] for j in range(len(cur_total)) if j != index]
    
    total_size = len(total_title) - 1

    tfidf_vec_simple = TfidfVectorizer()
    feature_vec_simple_total = tfidf_vec_simple.fit_transform(cur_total)
    feature_vec_dense_total = feature_vec_simple_total.todense()
    total_dense = feature_vec_dense_total[:total_size]
    total_mat = np.array(total_dense).T
    
    for i in range(len(summarizes)):
        vec_summarize = np.array(feature_vec_dense_total[total_size + i]).reshape(-1,)
        similarities = cos_similarity(vec_summarize, total_mat)
        similarity_simple.append(np.max(similarities))
        similarity_index.append(list(similarities).index(np.max(similarities)))
    similarity_max = max(similarity_simple)
    summarized_index = similarity_simple.index(similarity_max)
    
    return {'max_similarity': similarity_max, 
            'title_origin': title, 
            'title_selected': summarizes[summarized_index], 
            'index_of_selected': summarized_index,
            'summarizes': summarizes}


def main():
    print('start')
    total_title, total_sum = get_data(file)
    data = [(i, total_title, total_sum) for i in range(len(total_title))]
    result = apply_by_multiprocessor(data=data, func=extract_title, workers=6)
    print('end')
    
    pickle.dump(result, open('result.pkl', 'wb'))


if __name__ == '__main__':
    main()