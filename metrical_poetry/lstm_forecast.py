# coding: utf-8
import tensorflow as tf
from tensorflow.contrib import rnn

import data_set_word2vec


class LSTM(object):
    def __init__(self, poetry_type):
        self.poetry_type = poetry_type
        self.train_poetry, self.train_label, self.test_poetry, self.test_label = data_set_word2vec.train_test_set(
            self.poetry_type)

        self.n_classes = 4  # 输出的维度
        self.n_hidden = 128  # 一次训练多少组数据，也就是多少个cell
        self.n_step = [12, 16, 24, 32]  # 一首诗的长度
        self.learning_rate = 0.001
        self.n_input = 200
        self.batch_size = 32

        self.weights = {
            'out': tf.Variable(tf.random_normal([self.n_hidden, self.n_classes]))
        }
        self.biases = {
            'out': tf.Variable(tf.random_normal([self.n_classes]))
        }

    def RNN(self, x):
        x = tf.transpose(x, [1, 0, 2])
        x = tf.reshape(x, [-1, self.n_input])
        x = tf.split(x, self.n_step[self.poetry_type], 0)

        # 构建一个cell，暂时是照抄example
        lstm_cell = rnn.LSTMBlockCell(self.n_hidden, forget_bias=1.0)
        outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
        # matmul的功能是 output * weight + b
        return tf.matmul(outputs[-1], self.weights['out']) + self.biases['out']

    def run_test(self):
        # 预留输入，是 n * n_step * n_input 的输入
        x = tf.placeholder("float", [None, self.n_step[self.poetry_type], self.n_input])
        # 预留输出，是 n * n_classes
        y = tf.placeholder("float", [None, self.n_classes])
        # 暂时这些是照抄example
        pred = self.RNN(x)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(cost)
        correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        # Initializing the variables
        init = tf.global_variables_initializer()

        # Launch the graph
        with tf.Session() as sess:
            sess.run(init)
            for i in range(int(len(self.train_poetry) / self.batch_size) - 1):
                sess.run(optimizer,
                         feed_dict={x: self.train_poetry[i * self.batch_size:(i + 1) * self.batch_size],
                                    y: self.train_label[i * self.batch_size:(i + 1) * self.batch_size]})
                if i % 2 == 0:
                    acc = sess.run(accuracy,
                                   feed_dict={x: self.train_poetry[i * self.batch_size:(i + 1) * self.batch_size],
                                              y: self.train_label[i * self.batch_size:(i + 1) * self.batch_size]})
                    loss = sess.run(cost,
                                    feed_dict={x: self.train_poetry[i * self.batch_size:(i + 1) * self.batch_size],
                                               y: self.train_label[i * self.batch_size:(i + 1) * self.batch_size]})
                    print("Iter " + str(i) +
                          " \nacc: " + "{:.6f}".format(acc) +
                          " \nloss: " + "{:.5f}".format(loss))
            for i in range(int(len(self.test_poetry) / self.batch_size) - 1):
                print("Testing Accuracy:",
                      sess.run(accuracy, feed_dict={x: self.test_poetry[i * self.batch_size:(i + 1) * self.batch_size],
                                                    y: self.test_label[i * self.batch_size:(i + 1) * self.batch_size]}))


if __name__ == '__main__':
    my_test = LSTM(3)
    print("start")
    my_test.run_test()
