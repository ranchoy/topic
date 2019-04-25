# -*- coding: utf-8 -*-
import sys
import json
import queue
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
 

# algorithm_tree = dfs(rid=algorithm_id)
# print(algorithm_tree)

q = queue.Queue()

root = {}
root['id'] = '19776749'
root['name'] = topic_dict['19776749']['name']
root['value'] = topic_dict['19776749']['follow']
root['children'] = []


def level_traversal(rid, level=2):
    cur_level = 0
    if not isinstance(rid, str) or not topic_dict.get(rid):
        return []
    root['id'] = str(rid)
    root['name'] = topic_dict[str(rid)]['name']
    root['value'] = topic_dict[str(rid)]['follow']
    root['children'] = []
    q = queue.Queue()
    q.put(root)
    while not q.empty() and cur_level<=level:
        cur_level = cur_level + 1
        cur = q.get()
        for item in topic_son.get(cur['id'], []):
            temp = {}
            temp['id'] = str(item['id'])
            temp['name'] = item['name']
            temp['value'] = item['follow']
            temp['children'] = []
            cur['children'].append(temp)
            q.put(temp)
    return root
        
# 学科 19618774
#   人文学科 19649905 0
#   自然科学 19553298 1
#   文科 20206801 1
#   形式科学 19744646 1
#   社会科学 19551971
#   理科
 
data = level_traversal(rid='19776749', level=10) # 根话题
print(data)
print(type(data))
with open('./topic.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)