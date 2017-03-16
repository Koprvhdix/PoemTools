"""
create on 17-03-14
@author: Koprvhdix
"""

from segment import segment
import os
from metrical_poetry import MetricalPoetry
from dict_set import chapter_author_dict, author_time_dict, time_mark_dict


class LoadAllMetricalPoetry(object):
    """ Load All Poetry
    segment and embedding
    """

    def __init__(self):
        self.poetry_folder_path = '/Users/koprvhdix/Projects/graduation_project/PoemTools/poem'

    def load_poetry_by_params(self, poetry_type, need_time_label):
        """
        :param
        poetry_type: int, if poetry_type > 4, return all metrical poetry,
        else only return the poetry which has creative time.
        need_time_label: bool, True need to return time label
        :return:
        """
        poetry_list = list()
        label_list = list()
        for chapter in os.listdir(self.poetry_folder_path):
            chapter_path = self.poetry_folder_path + '/' + chapter

            author = chapter_author_dict[chapter]

            if poetry_type < 4 and author not in author_time_dict:
                    continue

            for poetry_file_name in os.listdir(chapter_path):
                poetry_file_open = open(chapter_path + '/' + poetry_file_name, "r", encoding="utf-8")

                poem_text = poetry_file_open.readlines()

                title_end_index = poem_text[0].find('\xa0')
                poem_text[0] = poem_text[0][title_end_index:]
                poem_text[0] = poem_text[0].replace('\xa0', '')
                poem_text[0] = poem_text[0].replace('\n', '')

                # delete the poetry which don't has space after the title in file
                # and there are other characters after the final full point.
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
                if poetry.is_metrical_poetry and poetry_type % 4 == poetry.poetry_type:
                    poetry_list.append(poetry)
                    if need_time_label:
                        label_list.append(time_mark_dict[author_time_dict[author]])

        sentences_list = segment(poetry_list)

        if need_time_label:
            return sentences_list, label_list
        else:
            return sentences_list
