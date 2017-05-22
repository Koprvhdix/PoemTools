"""
Created by Koprvhdix on 17/05/05
"""
from data.generation_data_set import generation_data_set, generation_train_set
from gensim.models import word2vec
from gensim import corpora, models
from generation.gan_model import ModelGAN
from data.load_PingShuiYun import LoadPingShuiYun
import tensorflow as tf
import logging
import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def embedding_poetry(model, poetry_set):
    answer = list()
    for poetry in poetry_set:
        poetry_embedding = list()
        sentence = list()
        for character in poetry:
            if character == '，' or character == '。':
                poetry_embedding.append(sentence)
                sentence = list()
            else:
                sentence.append(list(model[character]))
        answer.append(poetry_embedding)
    return answer


def embedding_word(model, word_set):
    answer = list()
    for word in word_set:
        word_embedding = list()
        for character in word:
            word_embedding.append(list(model[character]))
        answer.append(word_embedding)
    return answer


if __name__ == '__main__':
    PingShuiYun = LoadPingShuiYun()
    all_poetry_set, all_segment_set = generation_data_set(1)
    train_poetry_set = generation_train_set(1)
    print(train_poetry_set)

    # 获取准确分词
    lda_set = list()
    for i in range(len(train_poetry_set)):
        for j in range(len(all_poetry_set)):
            if train_poetry_set[i] == all_poetry_set[j]:
                lda_set.append(all_segment_set[j])
                break

    model = word2vec.Word2Vec(train_poetry_set, size=50, min_count=1)

    dictionary = corpora.Dictionary(lda_set)
    corpus = [dictionary.doc2bow(text) for text in lda_set]
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=10)

    poetry_key_word = list()
    for poetry in lda_set:
        corpus = dictionary.doc2bow(poetry)
        score_set = sorted(lda[corpus], key=lambda tup: -1 * tup[1])
        lda_split = lda.print_topic(score_set[0][0], topn=1000).split("*\"")
        word_set = ['', '', '', '']
        for i in range(len(lda_split)):
            if i != 0:
                word = lda_split[i][:lda_split[i].index('\"')]
                if len(word) == 2:
                    if word in poetry[0:4] and len(word_set[0]) == 0:
                        word_set[0] = word
                    if word in poetry[5:9] and len(word_set[1]) == 0:
                        word_set[1] = word
                    if word in poetry[10:14] and len(word_set[2]) == 0:
                        word_set[2] = word
                    if word in poetry[15:19] and len(word_set[3]) == 0:
                        word_set[3] = word
        poetry_key_word.append(word_set)

    key_word_embedding = list()
    for index in range(len(poetry_key_word)):
        key_word_embedding.append(embedding_word(model, poetry_key_word[index]))

    tone = [
        [['A', 'P', 'A', 'Z', 'Z', 'P', 'P'], ['A', 'Z', 'P', 'P', 'Z', 'Z', 'P'], ['A', 'Z', 'A', 'P', 'P', 'Z', 'Z'],
         ['A', 'P', 'A', 'Z', 'Z', 'P', 'P']],
        [['A', 'P', 'A', 'Z', 'P', 'P', 'Z'], ['A', 'Z', 'P', 'P', 'Z', 'Z', 'P'], ['A', 'Z', 'A', 'P', 'P', 'Z', 'Z'],
         ['A', 'P', 'A', 'Z', 'Z', 'P', 'P']],
        [['A', 'Z', 'P', 'P', 'Z', 'Z', 'P'], ['A', 'P', 'A', 'Z', 'Z', 'P', 'P'], ['A', 'P', 'A', 'Z', 'P', 'P', 'Z'],
         ['A', 'Z', 'P', 'P', 'Z', 'Z', 'P']],
        [['A', 'Z', 'A', 'P', 'P', 'Z', 'Z'], ['A', 'A', 'Z', 'Z', 'Z', 'P', 'P'], ['A', 'P', 'A', 'Z', 'P', 'P', 'Z'],
         ['A', 'Z', 'P', 'P', 'Z', 'Z', 'P']]]

    model_gan = ModelGAN()

    batch_size = 10

    init = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(init)

        poetry_embedding = embedding_poetry(model, train_poetry_set)

        discriminator_loss_list = list()
        for iter_num in range(10000):
            print("iter_num ", iter_num)
            step = 1
            discriminator_loss_before = discriminator_loss_list
            discriminator_loss = list()
            while step * batch_size <= 60:
                session.run(model_gan.opt_generator, feed_dict={
                    model_gan.key_word_list: key_word_embedding[(step - 1) * batch_size:step * batch_size],
                    model_gan.poetry_set: poetry_embedding[(step - 1) * batch_size:step * batch_size]})

                discriminator_loss = session.run(model_gan.discriminator_loss, feed_dict={
                    model_gan.key_word_list: key_word_embedding[(step - 1) * batch_size: step * batch_size],
                    model_gan.poetry_set: poetry_embedding[(step - 1) * batch_size:step * batch_size]})
                discriminator_loss_list.append(discriminator_loss)
                print("discriminator_loss: ", discriminator_loss)

                if discriminator_loss > 0.7 or iter_num % 10 == 9:
                    print(str(iter_num) + " file_output")
                    poetry = session.run(model_gan.output, feed_dict={
                        model_gan.key_word_list: key_word_embedding[(step - 1) * batch_size:step * batch_size]})
                    for poetry_index in range(batch_size):
                        poem_str = str()
                        for sentence_index in range(4):
                            character1_list = model.similar_by_vector(poetry[poetry_index][sentence_index][0], topn=100)
                            character2_list = model.similar_by_vector(poetry[poetry_index][sentence_index][1], topn=100)

                            character3_list = model.similar_by_vector(poetry[poetry_index][sentence_index][2], topn=100)
                            character4_list = model.similar_by_vector(poetry[poetry_index][sentence_index][3], topn=100)

                            character5_list = model.similar_by_vector(poetry[poetry_index][sentence_index][4], topn=100)
                            character6_list = model.similar_by_vector(poetry[poetry_index][sentence_index][5], topn=100)
                            character7_list = model.similar_by_vector(poetry[poetry_index][sentence_index][6], topn=100)

                            character_list = [[], [], [], [], [], [], []]
                            for i in range(100):
                                character_list[0].append(character1_list[i][0])
                                character_list[1].append(character2_list[i][0])
                                character_list[2].append(character3_list[i][0])
                                character_list[3].append(character4_list[i][0])
                                character_list[4].append(character5_list[i][0])
                                character_list[5].append(character6_list[i][0])
                                character_list[6].append(character7_list[i][0])

                            poem_str += str(character_list)
                            poem_str += '\n'

                        with open("file_" + str(iter_num) + "_" + str(step) + "_" + str(poetry_index), 'w', encoding='utf-8') as file_open:
                            file_open.write(poem_str)

                if discriminator_loss > 0.7:
                    session.run(model_gan.opt_discriminator, feed_dict={
                        model_gan.key_word_list: key_word_embedding[(step - 1) * batch_size:step * batch_size],
                        model_gan.poetry_set: poetry_embedding[(step - 1) * batch_size:step * batch_size]})
                    print("discriminator update")

                step += 1

            if iter_num % 10 == 9:
                time.sleep(30)
