# coding: utf-8
from gensim.models import word2vec
import os
from dict_set import author_time_dict, time_mark_dict, chapter_author_dict
from metrical_poetry import MetricalPoetry
import numpy as np
from segment import segment
import random


def train_test_set(poetry_type):
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'
    poetry_list = list()
    label_list = list()

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
            if poetry.is_metrical_poetry and poetry_type == poetry.poetry_type:
                poetry_list.append(poetry)
                label_list.append(time_mark_dict[author_time_dict[author]])

    sentences_list = segment(poetry_list)

    model = word2vec.Word2Vec(sentences_list, size=200, min_count=1)

    train_poetry = list()
    train_label = list()
    test_poetry = list()
    test_label = list()

    for i in range(len(sentences_list)):
        is_train = random.randint(0, 100)
        poetry_word_2_vec = list()

        for word in sentences_list[i]:
            poetry_word_2_vec.append(model[word])

        if is_train > 5:
            train_poetry.append(poetry_word_2_vec)
            train_label.append(label_list[i])
        else:
            test_poetry.append(poetry_word_2_vec)
            test_label.append(label_list[i])

    for random_time in range(len(train_poetry)):
        index1 = random.randint(0, len(train_poetry) - 1)
        index2 = random.randint(0, len(train_poetry) - 1)

        poetry = train_poetry[index1]
        train_poetry[index1] = train_poetry[index2]
        train_poetry[index2] = poetry

        label = train_label[index1]
        train_label[index1] = train_label[index2]
        train_label[index2] = label
    for random_time in range(len(test_poetry)):
        index1 = random.randint(0, len(test_poetry) - 1)
        index2 = random.randint(0, len(test_poetry) - 1)

        poetry = test_poetry[index1]
        test_poetry[index1] = test_poetry[index2]
        test_poetry[index2] = poetry

        label = test_label[index1]
        test_label[index1] = test_label[index2]
        test_label[index2] = label

    return train_poetry, train_label, test_poetry, test_label


if __name__ == '__main__':
    train_poetry, train_label, test_poetry, test_label = train_test_set(1)
    print(len(train_label))
    print(len(test_poetry))
