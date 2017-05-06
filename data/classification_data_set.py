"""
Created by Koprvhdix on 17/05/05
"""
import os
from data.dict_set import author_time_dict, time_mark_dict, chapter_author_dict
from data.metrical_poetry import MetricalPoetry
import random
from gensim.models import word2vec
from data.segment import segment


def random_data(data_set, label_set):
    if len(data_set) != len(label_set):
        return []

    for random_time in range(len(data_set)):
        index1 = random.randint(0, len(data_set) - 1)
        index2 = random.randint(0, len(data_set) - 1)

        poetry = data_set[index1]
        data_set[index1] = data_set[index2]
        data_set[index2] = poetry

        label = label_set[index1]
        label_set[index1] = label_set[index2]
        label_set[index2] = label

    return data_set, label_set


def embedding(model, poetry_set):
    data_set = list()
    for poetry in poetry_set:
        poetry_encode = list()
        sentence = list()
        for character in poetry:
            if character == '，' or character == '。':
                poetry_encode.append(sentence)
                sentence = list()
                continue
            sentence += list(model[character])
        data_set.append(poetry_encode)
    return data_set


def embedding_index(model, poetry_set):
    data_set = list()
    for poetry in poetry_set:
        poetry_encode = list()
        sentence = list()
        for character in poetry:
            if character == '，' or character == '。':
                poetry_encode.append(sentence)
                sentence = list()
                continue
            sentence.append(model[character])
        data_set.append(poetry_encode)
    return data_set


def classification_word2vec_data_set(poetry_type, is_segment):
    """
    抽取训练用的诗歌
    :param poetry_type: 0：五言绝句；1：七言绝句；2：五言律诗；3：七言律诗
    :param is_segment: 如果为True，则使用基于规则的分词，如果为False，则使用One-Hot方式
    :return: 
    """
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'

    total_list = list()

    total_poetry_list = list()
    total_label_list = list()

    train_poetry = list()
    train_label = list()
    test_poetry = list()
    test_label = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        author = chapter_author_dict[chapter]
        # 将没有年代标识的过滤掉
        if author not in author_time_dict:
            continue

        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem, encoding="utf-8")
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
                total_label_list.append(time_mark_dict[author_time_dict[author]])

                if is_segment:
                    total_poetry_list.append(poetry)
                    total_list.append(poetry)
                else:
                    total_poetry_list.append(poem_text[0])
                    total_list.append(poem_text[0])

    if is_segment:
        total_poetry_list = segment(total_poetry_list)
        total_list = segment(total_list)
        model = word2vec.Word2Vec(total_list, size=300, min_count=1)
    else:
        model = word2vec.Word2Vec(total_list, size=200, min_count=1)

    for i in range(len(total_poetry_list)):
        is_train = random.randint(0, 100)

        if is_train > 5:
            train_label.append(total_label_list[i])
            train_poetry.append(total_poetry_list[i])
        else:
            test_label.append(total_label_list[i])
            test_poetry.append(total_poetry_list[i])

    train_poetry = embedding(model, train_poetry)
    test_poetry = embedding(model, test_poetry)

    train_poetry_list, train_label_list = random_data(train_poetry, train_label)
    test_poetry_list, test_label_list = random_data(test_poetry, test_label)

    return train_poetry_list, train_label_list, test_poetry_list, test_label_list


def classification_index_code_data_set(poetry_type, is_segment):
    """
    抽取训练用的诗歌
    :param poetry_type: 0：五言绝句；1：七言绝句；2：五言律诗；3：七言律诗
    :param is_segment: 如果为True，则使用基于规则的分词，如果为False，则使用One-Hot方式
    :return: 
    """
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'

    total_list = list()

    total_poetry_list = list()
    total_label_list = list()

    train_poetry = list()
    train_label = list()
    test_poetry = list()
    test_label = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        author = chapter_author_dict[chapter]
        # 将没有年代标识的过滤掉
        if author not in author_time_dict:
            continue

        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem, encoding="utf-8")
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
                total_label_list.append(time_mark_dict[author_time_dict[author]])

                if is_segment:
                    total_poetry_list.append(poetry)
                    total_list.append(poetry)
                else:
                    total_poetry_list.append(poem_text[0])
                    total_list.append(poem_text[0])

    if is_segment:
        total_poetry_list = segment(total_poetry_list)
        total_list = segment(total_list)

    character_dict = dict()
    for poetry in total_list:
        for character in poetry:
            if character not in character_dict:
                character_dict[character] = 0
            character_dict[character] += 1

    new_character_list = sorted(character_dict.items(), key=lambda item: item[1])
    new_character_list.reverse()
    print(new_character_list)
    for i in range(len(new_character_list)):
        character_dict[new_character_list[i][0]] = i + 1

    for i in range(len(total_poetry_list)):
        is_train = random.randint(0, 100)

        if is_train > 5:
            train_label.append(total_label_list[i])
            train_poetry.append(total_poetry_list[i])
        else:
            test_label.append(total_label_list[i])
            test_poetry.append(total_poetry_list[i])

    train_poetry = embedding_index(character_dict, train_poetry)
    test_poetry = embedding_index(character_dict, test_poetry)

    train_poetry_list, train_label_list = random_data(train_poetry, train_label)
    test_poetry_list, test_label_list = random_data(test_poetry, test_label)

    return train_poetry_list, train_label_list, test_poetry_list, test_label_list
