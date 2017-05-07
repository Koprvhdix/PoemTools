"""
Created by Koprvhdix on 17/05/05
"""
from classification.model_lstm import ModelLSTM
from data.classification_data_set import classification_index_code_data_set, classification_word2vec_data_set
import tensorflow as tf


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
