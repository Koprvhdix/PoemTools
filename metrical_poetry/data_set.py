# coding:utf-8
import os
import random
from dict_set import author_time_dict, time_mark_dict, chapter_author_dict
from metrical_poetry import MetricalPoetry
import numpy as np


def get_char_set():
    """
    获取字符列表，构造稀疏矩阵
    :return:
    """
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'

    char_set = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem)
            poem_text = file_open.readlines()

            title_end_index = poem_text[0].find('\xa0')
            poem_text[0] = poem_text[0][title_end_index:]
            poem_text[0] = poem_text[0].replace('\xa0', '')
            poem_text[0] = poem_text[0].replace('\n', '')

            poetry = MetricalPoetry(poem_text[0])
            if poetry.is_metrical_poetry:
                poetry_char = list(poem_text[0])
                for item in poetry_char:
                    if item not in char_set:
                        char_set.append(item)
    return char_set


def train_test(poetry_type):
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'

    train_poetry = list()
    train_label = list()
    test_poetry = list()
    test_label = list()

    dict_char_set = get_char_set()

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
                is_train = random.randint(0, 100)

                # 构造稀疏矩阵
                poetry_char_matrix = list()
                for item in poem_text[0]:
                    one_char = np.zeros((len(dict_char_set)))
                    one_char[dict_char_set.index(item)] = 1
                    poetry_char_matrix.append(one_char)

                if len(poem_text[0]) != 32:
                    print(poem_text[0])

                if is_train > 33:
                    train_poetry.append(poetry_char_matrix)
                    train_label.append(time_mark_dict[author_time_dict[author]])
                else:
                    test_poetry.append(poetry_char_matrix)
                    test_label.append(time_mark_dict[author_time_dict[author]])
    return train_poetry, train_label, test_poetry, test_label


def not_recognize():
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'
    poetry_not_recognize = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        author = chapter_author_dict[chapter]
        # 将有年代标识的过滤掉
        if author in author_time_dict:
            continue

        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem)
            poem_text = file_open.readlines()

            title_end_index = poem_text[0].find('\xa0')
            poem_text[0] = poem_text[0][title_end_index:]
            poem_text[0] = poem_text[0].replace('\xa0', '')
            poem_text[0] = poem_text[0].replace('\n', '')

            poetry = MetricalPoetry(poem_text[0])
            if poetry.is_metrical_poetry:
                poetry_not_recognize.append(poem_text[0])
    return poetry_not_recognize


if __name__ == '__main__':
    train_poetry, train_label, test_poetry, test_label = train_test(1)
    print(len(train_poetry))
    print(len(train_label))
    print(len(test_poetry))
    print(len(test_label))
