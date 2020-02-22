from DataHandler.utils import apply_by_multiprocessor, save_data
from sklearn.feature_extraction.text import TfidfVectorizer
from Comparing.Similarity import cos_similarity
from DataHandler import ConfigHandler

import numpy as np
import pickle
import json


# Get summarized data and original title from article
def get_data(conf=None):
    data = pickle.load(open('clean_' + '{}.pkl'.format(conf['table']), 'rb'))

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

    cur_sum = total_sum[index]
    summarizes = cur_sum[0]
    sum_importance = cur_sum[1]
    title = total_title[index]
    sum_similarity = []
    similar_title_index = []
    cur_total = total_title + summarizes

    cur_total = [cur_total[j] for j in range(len(cur_total)) if j != index]

    total_size = len(total_title) - 1

    tfidf_vect_simple = TfidfVectorizer()
    feature_vect_simple_total = tfidf_vect_simple.fit_transform(cur_total)
    feature_vect_dense_total = feature_vect_simple_total.todense()
    total_dense = feature_vect_dense_total[:total_size]
    total_mat = np.array(total_dense).T

    for i in range(len(summarizes)):
        vect_summarize = np.array(feature_vect_dense_total[total_size + i]).reshape(-1, )
        similarities = cos_similarity(vect_summarize, total_mat)
        sum_similarity.append(np.max(similarities))
        similar_title_index.append(list(similarities).index(np.max(similarities)))

    sum_importance = [i / sum(sum_importance) for i in sum_importance]
    sum_similarity = [i / sum(sum_similarity) for i in sum_similarity]
    sum_weight = [sum_importance[i] + sum_similarity[i] for i in range(len(summarizes))]

    sorted_index = sorted(range(len(summarizes)), key=lambda i: sum_weight[i], reverse=True)
    sorted_importance = [sum_importance[i] for i in sorted_index]
    sorted_similarity = [sum_similarity[i] for i in sorted_index]
    sorted_weight = [sum_weight[i] for i in sorted_index]
    sorted_summary = [summarizes[i] for i in sorted_index]
    similar_titles = [cur_total[similar_title_index[i]] for i in sorted_index]

    return {'title_origin': title,
            'order_by_weight': sorted_index,
            'sorted_similarity': sorted_similarity,
            'sorted_importance': sorted_importance,
            'sorted_weight': sorted_weight,
            'sorted_summary': sorted_summary,
            'similar_titles': similar_titles}


def main():
    config = ConfigHandler.loadFromFile()
    total_title, total_sum = get_data(config)
    data = [(i, total_title, total_sum) for i in range(len(total_title))]
    result = apply_by_multiprocessor(data=data, func=extract_title)

    json.dump(result, open('result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()