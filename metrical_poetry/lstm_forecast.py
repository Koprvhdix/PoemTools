# coding: utf-8
import data_set
import tensorflow as tf
from tensorflow.contrib import rnn


class LSTM(object):
    def __init__(self, poetry_type):
        self.poetry_type = poetry_type
        self.train_poetry, self.train_label, self.test_poetry, self.test_label = data_set.train_test(self.poetry_type)

        self.train_poetry = self.train_poetry[:6500]
        self.train_label = self.train_label[:6500]

        self.n_classes = 4  # 输出的维度
        self.n_hidden = 2  # 一次训练多少组数据，也就是多少个cell
        self.n_step = [24, 32, 48, 64]  # 一首诗的长度
        self.learning_rate = 0.001
        self.n_input = 5772

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
            for i in range(3250):
                sess.run(optimizer,
                         feed_dict={x: self.train_poetry[i:(i + 1) * 2], y: self.train_label[i:(i + 1) * 2]})
                if i % 50 == 0:
                    acc = sess.run(accuracy, feed_dict={x: self.train_poetry[i:(i + 1) * 2],
                                                        y: self.train_label[i:(i + 1) * 2]})
                    loss = sess.run(cost, feed_dict={x: self.train_poetry[i:(i + 1) * 2],
                                                     y: self.train_label[i:(i + 1) * 2]})
                    print("Iter " + str(i) +
                          " \nacc: " + "{:.6f}".format(acc) +
                          " \nloss: " + "{:.5f}".format(loss))

            print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: self.test_poetry[:5], y: self.test_label[:5]}))


if __name__ == '__main__':
    my_test = LSTM(1)
    print("start")
    my_test.run_test()
