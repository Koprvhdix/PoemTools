# coding:utf-8


class MetricalPoetry(object):
    def __init__(self, poetry):
        self.poetry = poetry
        # 一句诗的字数，必须是5或者7
        self.key_char_number = 0
        self.poetry_type = -1
        self.is_metrical_poetry = self.recognize()
        # self.segmenter_list = self.segmenter()

    def recognize(self):
        char_number = 0
        # 必须是一个逗号一个句号
        punctuation_gate = 0
        # 必须只有两个句号或者4个句号
        sentence_number = 0
        for item in self.poetry:
            if item == '，':
                if punctuation_gate == 1:
                    return False
                punctuation_gate = 1

                if char_number != 7 and char_number != 5:
                    return False

                if self.key_char_number == 0:
                    self.key_char_number = char_number
                if char_number != self.key_char_number:
                    return False

                char_number = 0
            elif item == '。':
                if punctuation_gate == 0:
                    return False
                punctuation_gate = 0

                if char_number != 7 and char_number != 5 and char_number != self.key_char_number:
                    return False

                sentence_number += 1
                char_number = 0
            else:
                char_number += 1

        if sentence_number != 2 and sentence_number != 4:
            return False
        if sentence_number == 2:
            if self.key_char_number == 5:
                self.poetry_type = 0
            else:
                self.poetry_type = 1
        else:
            if self.key_char_number == 5:
                self.poetry_type = 2
            else:
                self.poetry_type = 3
        return True

    def segmenter(self):
        if not self.is_metrical_poetry:
            return list()
        if self.key_char_number == 5:
            word_list = list()
            index_pointer = 0
            word = str()
            for item in self.poetry:
                index_pointer += 1
                word += item
                if item == '，' or item == '。':
                    index_pointer = 0
                    word_list.append(word)
                    word = ''
                if index_pointer == 2 or index_pointer == 3 or index_pointer == 5 or index_pointer == 4:
                    word_list.append(word)
                    word = ''
            return word_list
        if self.key_char_number == 7:
            word_list = list()
            index_pointer = 0
            word = str()
            for item in self.poetry:
                index_pointer += 1
                word += item
                if item == '，' or item == '。':
                    index_pointer = 0
                    word_list.append(word)
                    word = ''
                if index_pointer == 2 or index_pointer == 4 or index_pointer == 5 or index_pointer == 6 or index_pointer == 7:
                    word_list.append(word)
                    word = ''
            return word_list

if __name__ == '__main__':
    metrical_poetry_test = MetricalPoetry('红军不怕远征难，万水千山只等闲。五岭逶迤腾细浪，乌蒙磅礴走泥丸。金沙水拍云崖暖，大渡桥横铁索寒。更喜岷山千里雪，三军过后尽开颜。')
    print(metrical_poetry_test.is_metrical_poetry)
    print(metrical_poetry_test.segmenter_list)
