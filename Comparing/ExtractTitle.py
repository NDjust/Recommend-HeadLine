import pickle
from DataHandler.utils import apply_by_multiprocessor
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


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


# Calculate cosine similarity between one summarization(v1) and all of the titles(v2)
def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm
    return similarity


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
    
    tfidf_vect_simple = TfidfVectorizer()
    feature_vect_simple_total = tfidf_vect_simple.fit_transform(cur_total)
    feature_vect_dense_total = feature_vect_simple_total.todense()
    total_dense = feature_vect_dense_total[:total_size]
    total_mat = np.array(total_dense).T
    
    for i in range(len(summarizes)):
        vect_summarize = np.array(feature_vect_dense_total[total_size + i]).reshape(-1,)
        similarities = cos_similarity(vect_summarize, total_mat)
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