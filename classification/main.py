"""
Created by Koprvhdix on 17/05/05
"""
from classification.model_lstm import ModelLSTM
from data.classification_data_set import classification_index_code_data_set, classification_word2vec_data_set
import tensorflow as tf

import os
from data.dict_set import author_time_dict, time_mark_dict, chapter_author_dict
from data.metrical_poetry import MetricalPoetry
import random
from gensim.models import word2vec
from data.segment import segment


def train_test(poetry_type):
    poem_path = '/Users/koprvhdix/Projects/PoemTools/poem'

    total_list = list()

    train_poetry = list()
    train_label = list()
    test_poetry = list()
    test_label = list()

    for chapter in os.listdir(poem_path):
        chapter_path = poem_path + '/' + chapter

        author = chapter_author_dict[chapter]
        # 将没有年代标识的过滤掉
        if author not in author_time_dict:
            continue

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

            total_list.append(poem_text[0])

            poetry = MetricalPoetry(poem_text[0])
            if poetry.is_metrical_poetry and poetry_type == poetry.poetry_type:
                is_train = random.randint(0, 100)

                if is_train > 5:
                    train_poetry.append(poem_text[0])
                    train_label.append(time_mark_dict[author_time_dict[author]])
                else:
                    test_poetry.append(poem_text[0])
                    test_label.append(time_mark_dict[author_time_dict[author]])

    model = word2vec.Word2Vec(total_list, size=200, min_count=1)

    train_poetry_encode = list()
    test_poetry_encode = list()
    for poetry in train_poetry:
        poetry_encode = list()
        sentence = list()
        for character in poetry:
            if character == '，' or character == '。':
                poetry_encode.append(sentence)
                sentence = list()
                continue
            sentence += list(model[character])
        train_poetry_encode.append(poetry_encode)

    for poetry in test_poetry:
        poetry_encode = list()
        sentence = list()
        for character in poetry:
            if character == '，' or character == '。':
                poetry_encode.append(sentence)
                sentence = list()
                continue
            sentence += list(model[character])
        test_poetry_encode.append(poetry_encode)

    for random_time in range(len(train_poetry_encode)):
        index1 = random.randint(0, len(train_poetry_encode) - 1)
        index2 = random.randint(0, len(train_poetry_encode) - 1)

        poetry = train_poetry_encode[index1]
        train_poetry_encode[index1] = train_poetry_encode[index2]
        train_poetry_encode[index2] = poetry

        label = train_label[index1]
        train_label[index1] = train_label[index2]
        train_label[index2] = label
    for random_time in range(len(test_poetry_encode)):
        index1 = random.randint(0, len(test_poetry_encode) - 1)
        index2 = random.randint(0, len(test_poetry_encode) - 1)

        poetry = test_poetry_encode[index1]
        test_poetry_encode[index1] = test_poetry_encode[index2]
        test_poetry_encode[index2] = poetry

        label = test_label[index1]
        test_label[index1] = test_label[index2]
        test_label[index2] = label

    return train_poetry_encode, train_label, test_poetry_encode, test_label


if __name__ == '__main__':
    poetry_type = 3
    n_input = 7
    n_step = 8
    n_classes = 4

    model = ModelLSTM(n_input, n_step, n_classes)

    train_poetry_list, train_label_list, test_poetry_list, test_label_list = classification_index_code_data_set(
        poetry_type, False)

    batch_size = 32

    # Initializing the variables
    init = tf.global_variables_initializer()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        for train_time in range(1):
            for i in range(int(len(train_poetry_list) // batch_size)):
                sess.run(model.optimizer,
                         feed_dict={model.data: train_poetry_list[i * batch_size:(i + 1) * batch_size],
                                    model.label: train_label_list[i * batch_size:(i + 1) * batch_size]})
                if i % 10 == 0:
                    print(sess.run(tf.argmax(model.output, 1),
                                   feed_dict={model.data: train_poetry_list[i * batch_size:(i + 1) * batch_size]}))
                    print(sess.run(tf.argmax(model.label, 1),
                                   feed_dict={model.label: train_label_list[i * batch_size:(i + 1) * batch_size]}))
                    acc = sess.run(model.accuracy,
                                   feed_dict={model.data: train_poetry_list[i * batch_size:(i + 1) * batch_size],
                                              model.label: train_label_list[i * batch_size:(i + 1) * batch_size]})
                    loss = sess.run(model.cost,
                                    feed_dict={model.data: train_poetry_list[i * batch_size:(i + 1) * batch_size],
                                               model.label: train_label_list[i * batch_size:(i + 1) * batch_size]})
                    print("Iter " + str(i) +
                          " \nacc: " + "{:.6f}".format(acc) +
                          " \nloss: " + "{:.5f}".format(loss))
        for i in range(int(len(test_poetry_list) // batch_size)):
            print("Testing Accuracy:",
                  sess.run(model.accuracy,
                           feed_dict={model.data: test_poetry_list[i * batch_size:(i + 1) * batch_size],
                                      model.label: test_label_list[
                                                   i * batch_size:(i + 1) * batch_size]}))
            print(sess.run(tf.argmax(model.output, 1),
                           feed_dict={model.data: test_poetry_list[i * batch_size:(i + 1) * batch_size]}))
            print(sess.run(tf.argmax(model.label, 1),
                           feed_dict={model.label: test_label_list[i * batch_size:(i + 1) * batch_size]}))
