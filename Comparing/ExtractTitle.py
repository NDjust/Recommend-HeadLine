from DataHandler.utils import apply_by_multiprocessor, handle_pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from Comparing.Similarity import cos_similarity
from DataHandler import ConfigHandler

import numpy as np
import pickle
import json


# Get summarized data and original title from article
def get_data():
    conf = ConfigHandler.loadFromFile()
    data = handle_pickle('clean_' + '{}.pkl'.format(conf['title_table']))

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
def extract_from_title_content_pair(data):
    index = data[0]
    total_title = data[1]
    total_sum = data[2]

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
    if sum(sum_similarity) > 0:
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


def extract_from_content(data):
    cur_sum = data[0]
    total_title = data[1]

    summarizes = cur_sum[0]
    sum_importance = cur_sum[1]
    sum_similarity = []
    similar_title_index = []
    cur_total = total_title + summarizes

    total_size = len(total_title)

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
    if sum(sum_similarity) > 0:
        sum_similarity = [i / sum(sum_similarity) for i in sum_similarity]
    sum_weight = [sum_importance[i] + sum_similarity[i] for i in range(len(summarizes))]

    sorted_index = sorted(range(len(summarizes)), key=lambda i: sum_weight[i], reverse=True)
    sorted_importance = [sum_importance[i] for i in sorted_index]
    sorted_similarity = [sum_similarity[i] for i in sorted_index]
    sorted_weight = [sum_weight[i] for i in sorted_index]
    sorted_summary = [summarizes[i] for i in sorted_index]
    similar_titles = [cur_total[similar_title_index[i]] for i in sorted_index]

    return {'order_by_weight': sorted_index,
            'sorted_similarity': sorted_similarity,
            'sorted_importance': sorted_importance,
            'sorted_weight': sorted_weight,
            'sorted_summary': sorted_summary,
            'similar_titles': similar_titles}


def extract_from_origin_title():
    total_title, total_sum = get_data()
    data = [(i, total_title, total_sum) for i in range(len(total_title))]
    result = apply_by_multiprocessor(data=data, func=extract_from_title_content_pair)

    json.dump(result, open('result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


def extract_from_given_title():
    conf = ConfigHandler.loadFromFile()
    total_title = handle_pickle('title_{}.pkl'.format(conf['title_table']))
    total_sum = handle_pickle('clean_content_{}.pkl'.format(conf['content_table']))
    data = [(total_sum[i], total_title) for i in range(len(total_sum))]
    result = apply_by_multiprocessor(data=data, func=extract_from_content)

    json.dump(result, open('result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)



def main():
    pass


if __name__ == '__main__':
    main()