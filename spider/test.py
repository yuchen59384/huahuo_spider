import os

import jieba


def load_brands_dict():  # 读取文件，获取brand字典
    crawler_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    brands_dict_file = os.path.join(os.path.join(crawler_path, 'res'), 'brands_with_alias.txt')
    brands_official_map = {}
    with open(brands_dict_file, 'r',encoding='UTF-8') as f:
        for line in f.readlines():
            brands_with_syn = line.strip().split('\t')
            brand_main = brands_with_syn[0]
            for b in brands_with_syn:
                brands_official_map[b.lower()] = brand_main
    return brands_official_map

def get_note_brand(title,tags): #获取品牌
    for b in brands_dict:
        jieba.add_word(b)
    brands = []
    for word in jieba.cut(title):
        if word.lower() in brands_dict:
            brands.append(brands_dict[word.lower()])
    for tag in tags:
        if tag.lower() in brands_dict:
            brands.append(brands_dict[tag.lower()])
    return brands

title= "终极自热火锅测评之自嗨锅！这绝对是我吃过最好吃的自热火锅了！"
brands_dict=load_brands_dict()
tags=['邦臣','veidoo','铂顿','虹雅堂','凯霓	carrian','mokopoio']
print(get_note_brand(title,tags))