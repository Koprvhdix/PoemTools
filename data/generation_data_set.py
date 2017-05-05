"""
Created by Koprvhdix on 17/05/05
"""

import os
from data.metrical_poetry import MetricalPoetry


def generation_data_set(poetry_type):
    poem_path = '/Users/koprvhdix/Projects/GraduationProject/poem'
    data_set = list()
    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

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
                data_set.append(poem_text[0])

    return data_set


if __name__ == '__main__':
    train_set = generation_data_set(0)
    print('type 0:', len(train_set))
    train_set = generation_data_set(1)
    print('type 1:', len(train_set))
    train_set = generation_data_set(2)
    print('type 2:', len(train_set))
    train_set = generation_data_set(3)
    print('type 3:', len(train_set))
