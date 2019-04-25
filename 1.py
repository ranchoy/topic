# -*- coding: utf-8 -*-
import sys
import pickle

sys.setrecursionlimit(1000000) # 设置递归最大次数

# mysql数据形式
# 数据字段：(id, pid, name, follows)
# 具体数据：(19550638, '19562033,20048648,20045637', '社交网络', 1844080)


topic = pickle.load(open('./topic.pkl', 'rb')) # topic元组，数据库中原始数据，如topic[0] = (19550638, '19562033,20048648,20045637', '社交网络', 1844080)
topic_dict = pickle.load(open('./topic_dict.pkl', 'rb')) # topic字典，如topic_dict['19776749'] = {'name': '「根话题」', 'follow': 156378}
topic_son = pickle.load(open('./topic_son.pkl', 'rb')) # topic_son字典


def dfs(rid):
    res = {}
    res['name'] = topic_dict[rid]['name']
    res['value'] = topic_dict[rid]['follow']
    if topic_son[rid]:
        res['children'] = []
    for item in topic_son[rid]:
        temp = {}
        temp['name'] = item['name']
        temp['value'] = item['follow']
        temp['children'] = dfs(str(item['id']))
        
        res['children'].append(temp)  
    return res


root_id = '19776749' # 根话题（不能递归）

algorithm_id = '19553510' # 算法 话题（可以递归）

subject_id = '19618774' # 学科 话题（不能递归）
 

algorithm_tree = dfs(rid=algorithm_id)
print(algorithm_tree)

