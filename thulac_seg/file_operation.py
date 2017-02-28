# coding：utf-8
import os
import json


class poems(object):
    def __init__(self):
        self.poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'
        self.output_path = '/Users/koprvhdix/Projects/PoemTools/thulac_seg_file'

    def get_poem(self):
        poem_text_list = list()
        for chapter in os.listdir(self.poem_path):
            chapter_path = self.poem_path + '/' + chapter
            for poem in os.listdir(chapter_path):
                file_open = open(chapter_path + '/' + poem)
                poem_text = file_open.readlines()

                title_end_index = poem_text[0].find('\xa0')
                poem_text[0] = poem_text[0][title_end_index:]
                poem_text[0] = poem_text[0].replace('\xa0', '')
                poem_text[0] = poem_text[0].replace('\n', '')

                poem_text_list.append(poem_text[0])
        return poem_text_list

    def write_poem_vector(self, poem_vector_list):
        file_open = open(self.output_path, 'w')
        file_open.writelines(json.dumps(poem_vector_list))


# test
if __name__ == '__main__':
    poems = poems()
    poems.get_poem()
