"""
Created by Koprvhdix on 17/05/05
"""
import tensorflow as tf
from tensorflow.contrib import rnn


class ModelLSTM(object):
    def __init__(self, n_input, n_step, n_classes):
        self.n_input = n_input
        self.n_step = n_step
        self.n_hidden = 1024
        self.n_classes = n_classes
        self.learning_rate = 0.001

        self.data = tf.placeholder("float", [None, self.n_step, self.n_input])
        self.label = tf.placeholder("float", [None, self.n_classes])
        weights = tf.Variable(tf.random_normal([self.n_hidden, self.n_classes]))
        biases = tf.Variable(tf.random_normal([self.n_classes]))

        data = tf.transpose(self.data, [1, 0, 2])
        data = tf.reshape(data, [-1, self.n_input])
        data = tf.split(data, self.n_step, 0)

        lstm_cell = rnn.LSTMCell(self.n_hidden, forget_bias=1.0, use_peepholes=True)
        outputs, states = rnn.static_rnn(lstm_cell, data, dtype=tf.float32)

        self.output = tf.matmul(outputs[-1], weights) + biases
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.output, labels=self.label))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
        correct_pred = tf.equal(tf.argmax(self.output, 1), tf.argmax(self.label, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
