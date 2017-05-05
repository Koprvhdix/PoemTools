# coding:utf-8


class MetricalPoetry(object):
    def __init__(self, poetry):
        self.poetry = poetry
        # 一句诗的字数，必须是5或者7
        self.key_char_number = 0
        self.poetry_type = -1
        self.is_metrical_poetry = self.recognize()

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

                if (char_number != 7 and char_number != 5) or char_number != self.key_char_number:
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

if __name__ == '__main__':
    metrical_poetry_test = MetricalPoetry('雄鹄衔枝来，雌鹄啄泥归。巢成不生子，大义当乖离。江汉水之大，鹄身鸟之微。更无相逢日，且可绕树相随飞。')
    print(metrical_poetry_test.is_metrical_poetry)
