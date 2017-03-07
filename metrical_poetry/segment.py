# coding: utf-8


def segment(metrical_poetry):
    word_list = dict()
    for poetry in metrical_poetry:
        if not poetry.is_metrical_poetry:
            continue
        if poetry.key_char_number == 5:
            index_pointer = 0
            word = str()
            for item in poetry.poetry:
                index_pointer += 1
                word += item
                if item == '，' or item == '。':
                    index_pointer = 0
                    word = ''
                    continue
                if index_pointer == 2:
                    if word not in word_list:
                        word_list[word] = 1
                    else:
                        word_list[word] += 1
                    word = ''
        if poetry.key_char_number == 7:
            index_pointer = 0
            word = str()
            for item in poetry.poetry:
                index_pointer += 1
                word += item
                if item == '，' or item == '。':
                    index_pointer = 0
                    word = ''
                    continue
                if index_pointer == 2 or index_pointer == 4:
                    if word not in word_list:
                        word_list[word] = 1
                    else:
                        word_list[word] += 1
                    word = ''

    sentence_list = list()
    for poetry in metrical_poetry:
        sentence = list()
        if not poetry.is_metrical_poetry:
            continue
        if poetry.key_char_number == 5:
            index_pointer = 0
            word = str()
            for i in range(len(poetry.poetry)):
                index_pointer += 1
                if poetry.poetry[i] == '，' or poetry.poetry[i] == '。':
                    word1 = poetry.poetry[i - 3:i - 1]
                    word2 = poetry.poetry[i - 2:i]

                    if word1 in word_list and word2 in word_list:
                        if word_list[word1] >= word_list[word2]:
                            sentence.append(word1)
                            sentence.append(poetry.poetry[i - 1])
                        else:
                            sentence.append(poetry.poetry[i - 3])
                            sentence.append(word2)
                    elif word1 not in word_list and word2 in word_list:
                        sentence.append(poetry.poetry[i - 3])
                        sentence.append(word2)
                    elif word1 in word_list and word2 not in word_list:
                        sentence.append(word1)
                        sentence.append(poetry.poetry[i - 1])
                    else:
                        sentence.append(word1)
                        sentence.append(poetry.poetry[i - 1])

                    index_pointer = 0
                    word = ''
                    continue
                word += poetry.poetry[i]
                if index_pointer == 2:
                    sentence.append(word)
                    word = ''
        if poetry.key_char_number == 7:
            index_pointer = 0
            word = str()
            for i in range(len(poetry.poetry)):
                index_pointer += 1
                if poetry.poetry[i] == '，' or poetry.poetry[i] == '。':
                    word1 = poetry.poetry[i - 3:i - 1]
                    word2 = poetry.poetry[i - 2:i]

                    if word1 in word_list and word2 in word_list:
                        if word_list[word1] >= word_list[word2]:
                            sentence.append(word1)
                            sentence.append(poetry.poetry[i-1])
                        else:
                            sentence.append(poetry.poetry[i - 3])
                            sentence.append(word2)
                    elif word1 not in word_list and word2 in word_list:
                        sentence.append(poetry.poetry[i - 3])
                        sentence.append(word2)
                    elif word1 in word_list and word2 not in word_list:
                        sentence.append(word1)
                        sentence.append(poetry.poetry[i - 1])
                    else:
                        sentence.append(word1)
                        sentence.append(poetry.poetry[i - 1])

                    index_pointer = 0
                    word = ''
                    continue
                word += poetry.poetry[i]
                if index_pointer == 2 or index_pointer == 4:
                    sentence.append(word)
                    word = ''
        sentence_list.append(sentence)
    return sentence_list
