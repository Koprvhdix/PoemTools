# coding: utf-8

from gensim.models import word2vec
import os
from dict_set import author_time_dict, time_mark_dict, chapter_author_dict
from metrical_poetry import MetricalPoetry
import numpy as np
from segment import segment


if __name__ == '__main__':
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'
    poetry_list = list()
    sentences = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        author = chapter_author_dict[chapter]
        # 将没有年代标识的过滤掉
        if author not in author_time_dict:
            continue

        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem)
            poem_text = file_open.readlines()

            title_end_index = poem_text[0].find('\xa0')
            poem_text[0] = poem_text[0][title_end_index:]
            poem_text[0] = poem_text[0].replace('\xa0', '')
            poem_text[0] = poem_text[0].replace('\n', '')

            # 处理奇怪的诗
            if len(poem_text[0]) == 0:
                continue
            elif poem_text[0][-1] != '。':
                index = 0
                while True:
                    index = poem_text[0].find('。', index + 1)
                    if poem_text[0].find('。', index + 1) == -1:
                        break
                poem_text[0] = poem_text[0][:index + 1]

            poetry = MetricalPoetry(poem_text[0])
            if poetry.is_metrical_poetry:
                poetry_list.append(poetry)

    sentences_list = segment(poetry_list)

    model = word2vec.Word2Vec(sentences_list, size=200)
    y1 = model.similarity("今日", "明月")
    print(model["今日"])
