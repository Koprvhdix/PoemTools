import tensorflow as tf
from tensorflow.contrib import rnn
from data.load_PingShuiYun import LoadPingShuiYun


class ModelGAN(object):
    def __init__(self):
        self.PingShuiYun = LoadPingShuiYun()
        self.n_input = self.n_hidden = 512

        self.word_num = 4
        self.char_num = 2

        with tf.variable_scope('encoder_decoder') as encoder_decoder_scope:
            # batch_size, word_num, char_num, input_size
            self.key_word_list = tf.placeholder(tf.float32, [None, self.word_num, self.char_num, self.n_input])

            key_word_list = tf.transpose(self.key_word_list, [1, 0, 2, 3])
            key_word_list = tf.reshape(key_word_list, [-1, self.char_num, self.n_input])
            key_word_list = tf.split(key_word_list, self.word_num, 0)

            fw_key_word_encoder_1, bw_key_word_encoder_1 = self.key_word_encoder(key_word_list[0], self.char_num)
            self.key_word_encoder_1 = self.encoder([fw_key_word_encoder_1], [bw_key_word_encoder_1])

            # decoder_input shape (7, ?, 512)
            self.decoder_input_1 = tf.concat(
                [self.key_word_encoder_1, self.key_word_encoder_1, self.key_word_encoder_1, self.key_word_encoder_1,
                 self.key_word_encoder_1, self.key_word_encoder_1, self.key_word_encoder_1], 0)

            # output_1 list length 7, each item (?, 512)
            self.output_fw_1 = self.decoder(self.decoder_input_1, 7)

            output_fw = list()
            output_bw = list()
            for i in range(7):
                output_fw.append(self.output_fw_1[i])
                output_bw.append(self.output_fw_1[6 - i])

            # 重新使用变量
            encoder_decoder_scope.reuse_variables()

            # 第二句
            fw_key_word_encoder_2, bw_key_word_encoder_2 = self.key_word_encoder(key_word_list[1], self.char_num)
            key_word_encoder_2 = self.encoder([fw_key_word_encoder_2], [bw_key_word_encoder_2])
            sentence_before_2 = self.encoder(output_fw, output_bw)
            sentence_before_2_list = tf.split(sentence_before_2, 7)

            decoder_input_2 = list()
            for i in range(7):
                decoder_input_2.append(key_word_encoder_2)
                for j in range(7):
                    decoder_input_2[i] += sentence_before_2_list[j]
                decoder_input_2[i] /= 8

            self.output_fw_2 = self.decoder(decoder_input_2, 7)

            for i in range(7):
                output_fw.append(self.output_fw_2[i])
                output_bw.append(self.output_fw_2[6 - i])

            encoder_decoder_scope.reuse_variables()

            # 第三句
            fw_key_word_encoder_3, bw_key_word_encoder_3 = self.key_word_encoder(key_word_list[2], self.char_num)
            key_word_encoder_3 = self.encoder([fw_key_word_encoder_3], [bw_key_word_encoder_3])
            sentence_before_3 = self.encoder(output_fw, output_bw)
            sentence_before_3_list = tf.split(sentence_before_3, 14)

            decoder_input_3 = list()
            for i in range(7):
                decoder_input_3.append(key_word_encoder_3)
                for j in range(14):
                    decoder_input_2[i] += sentence_before_3_list[j]
                decoder_input_3[i] /= 15

            self.output_fw_3 = self.decoder(decoder_input_3, 7)

            for i in range(7):
                output_fw.append(self.output_fw_3[i])
                output_bw.append(self.output_fw_3[6 - i])

            encoder_decoder_scope.reuse_variables()

            # 第四句
            fw_key_word_encoder_4, bw_key_word_encoder_4 = self.key_word_encoder(key_word_list[3], self.char_num)
            key_word_encoder_4 = self.encoder([fw_key_word_encoder_4], [bw_key_word_encoder_4])
            sentence_before_4 = self.encoder(output_fw, output_bw)
            sentence_before_4_list = tf.split(sentence_before_4, 21)

            decoder_input_4 = list()
            for i in range(7):
                decoder_input_4.append(key_word_encoder_4)
                for j in range(21):
                    decoder_input_4[i] += sentence_before_4_list[j]
                decoder_input_4[i] /= 22

            self.output_fw_4 = self.decoder(decoder_input_4, 7)

        with tf.variable_scope('discriminator') as discriminator_scope:
            self.poetry_set = tf.placeholder(tf.float32, [None, 4, 7, self.n_input])
            poetry_set = tf.reshape(self.poetry_set, [-1, 7 * self.n_input])
            poetry_set = tf.split(poetry_set, 4, 0)

            generate_poetry = [[], [], [], []]
            for i in range(7):
                generate_poetry[0].append(self.output_fw_1[i])
                generate_poetry[1].append(self.output_fw_2[i])
                generate_poetry[2].append(self.output_fw_3[i])
                generate_poetry[3].append(self.output_fw_4[i])
            generate_poetry = tf.transpose(generate_poetry, [2, 0, 1, 3])
            self.output = generate_poetry
            generate_poetry = tf.reshape(generate_poetry, [-1, 7 * self.n_input])
            generate_poetry = tf.split(generate_poetry, 4, 0)

            self.human_discriminator = self.discriminator(poetry_set)
            discriminator_scope.reuse_variables()
            self.ai_discriminator = self.discriminator(generate_poetry)

            var_scope = tf.trainable_variables()
            self.encoder_decoder_params = list()
            self.discriminator_params = list()
            for v in var_scope:
                if v.name.startswith('encoder_decoder/'):
                    self.encoder_decoder_params.append(v)
                else:
                    self.discriminator_params.append(v)

            self.generate_loss = tf.reduce_mean(tf.log(self.human_discriminator) + tf.log(1 - self.ai_discriminator))
            self.discriminator_loss = tf.reduce_mean(
                -tf.log(self.human_discriminator) - tf.log(1 - self.ai_discriminator))

            self.opt_discriminator = tf.train.GradientDescentOptimizer(0.005).minimize(self.discriminator_loss,
                                                                                       var_list=self.discriminator_params)
            self.opt_generator = tf.train.GradientDescentOptimizer(0.005).minimize(self.generate_loss,
                                                                                   var_list=self.encoder_decoder_params)

    def key_word_encoder(self, x, n_step):
        """
        用于关键词的encoder
        :param x: [batch_size, 2, self.n_input], int自动转float, 将字向量转成两倍的state向量
        :param n_step: int 步长
        :return: [batch_size, self.hidden]
        """
        bw_x = tf.reverse(x, [1])

        x = tf.transpose(x, [1, 0, 2])
        x = tf.reshape(x, [-1, self.n_input])
        x = tf.split(x, n_step, 0)

        bw_x = tf.transpose(bw_x, [1, 0, 2])
        bw_x = tf.reshape(bw_x, [-1, self.n_input])
        bw_x = tf.split(bw_x, n_step, 0)

        with tf.variable_scope('key_forward'):
            # Forward direction cell
            lstm_fw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
            fw_outputs, fw_states = rnn.static_rnn(lstm_fw_cell, x, dtype=tf.float32)
        with tf.variable_scope('key_backward'):
            # Backward direction cell
            lstm_bw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
            bw_outputs, bw_states = rnn.static_rnn(lstm_bw_cell, bw_x, dtype=tf.float32)

        return fw_outputs[-1], bw_outputs[-1]

    def encoder(self, fw_x, bw_x):
        """
        句子的encoder
        :param fw_x: 前向序列
        :param bw_x: 反向序列
        :param n_step: 变步长
        :return: 
        """
        with tf.variable_scope('forward'):
            # Forward direction cell
            lstm_fw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
            fw_outputs, fw_states = rnn.static_rnn(lstm_fw_cell, fw_x, dtype=tf.float32)
        with tf.variable_scope('backward'):
            # Backward direction cell
            lstm_bw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
            bw_outputs, bw_states = rnn.static_rnn(lstm_bw_cell, bw_x, dtype=tf.float32)

        bw_outputs = tf.reverse(bw_outputs, [1])
        bi_outputs = fw_outputs + bw_outputs
        return bi_outputs

    def decoder(self, x, n_step):
        """
        :param x: 
        :param n_step: 
        :return: 
        """
        x = tf.reshape(x, [-1, 512])
        x = tf.split(x, n_step, 0)

        lstm_fw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
        output, states = rnn.static_rnn(lstm_fw_cell, x, dtype=tf.float32)

        return output

    def discriminator(self, x):
        weight = tf.Variable(tf.random_normal([self.n_hidden, 1]))
        biase = tf.Variable(tf.random_normal([1]))

        lstm_fw_cell = rnn.BasicLSTMCell(self.n_hidden, forget_bias=1.0)
        output, states = rnn.static_rnn(lstm_fw_cell, x, dtype=tf.float32)

        return tf.sigmoid(tf.matmul(output[-1], weight) + biase)
