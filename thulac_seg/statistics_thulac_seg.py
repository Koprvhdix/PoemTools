# coding:utf-8
import json

if __name__ == '__main__':
    seg_result_file = '/Users/koprvhdix/Projects/PoemTools/thulac_seg_file'
    file_open = open(seg_result_file)
    poem_text = file_open.readlines()
    poem_text = json.loads(poem_text[0])

    word_dict = dict()
    for poem in poem_text:
        for word in poem:
            if len(word) == 2:
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1

    print(sorted(word_dict.items(), key=lambda d: d[1], reverse=True)[:500])
