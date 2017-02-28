# coding: utf-8
import os
from metrical_poetry import MetricalPoetry


def poetry_remove_title():
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'
    poem_text_list = list()
    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter
        for poem in os.listdir(chapter_path):
            file_open = open(chapter_path + '/' + poem)
            poem_text = file_open.readlines()

            title_end_index = poem_text[0].find('\xa0')
            poem_text[0] = poem_text[0][title_end_index:]
            poem_text[0] = poem_text[0].replace('\xa0', '')
            poem_text[0] = poem_text[0].replace('\n', '')

            poem_text_list.append(poem_text[0])
    return poem_text_list


if __name__ == '__main__':
    poetry_set = poetry_remove_title()
    # 统计格律诗的数量
    count_metrical_poetry = 0
    # 单字词和双字词
    word_dict1 = dict()
    word_dict2 = dict()

    for item in poetry_set:
        poetry_item = MetricalPoetry(item)
        if poetry_item.is_metrical_poetry:
            count_metrical_poetry += 1
            for word in poetry_item.segmenter_list:
                if len(word) == 2:
                    if word not in word_dict2:
                        word_dict2[word] = 1
                    else:
                        word_dict2[word] += 1
                else:
                    if word not in word_dict1:
                        word_dict1[word] = 1
                    else:
                        word_dict1[word] += 1

    print(count_metrical_poetry)
    print(sorted(word_dict1.items(), key=lambda d: d[1], reverse=True))
    print(sorted(word_dict2.items(), key=lambda d: d[1], reverse=True))
