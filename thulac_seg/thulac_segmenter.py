# coding:utf-8

import thulac
from file_operation import poems

poem = poems()
poem_text_list = poem.get_poem()

thu1 = thulac.thulac(seg_only=True)

poem_vector_list = list()
# 诗的数量
number = 0
for poem_text in poem_text_list:
    text = thu1.cut(poem_text)
    new_poetry = list()
    for item in text:
        new_poetry.append(item[0])
    poem_vector_list.append(new_poetry)
    number += 1
    print(number)

print(number)
poem.write_poem_vector(poem_vector_list)
