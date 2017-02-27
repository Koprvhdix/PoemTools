# coding:utf-8

import thulac
from file_operation import poems


poem = poems()
poem_text_list = poem.get_poem()

thu1 = thulac.thulac(seg_only=True)

poem_vector_list = str()
number = 0
for poem_text in poem_text_list:
    text = thu1.cut(poem_text)
    poem_vector_list += str([item[0] for item in text])
    poem_vector_list += '\n'
    number += 1
    print(number)
poem.write_poem_vector(poem_vector_list)
