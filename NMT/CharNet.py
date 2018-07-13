# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 01:20:08 2018

@author: derong
"""

import tensorflow as tf

class CharNet():
    def __init__(self, batch_size, seq_length, lstm_size, keep_prob, num_classes,
                 num_layers, learning_rate=0.001, training=True):
        
        tf.reset_default_graph()
        
        if not training:
            batch_size = 1
            seq_length = 1

        
        self.inputs, self.targets = self.build_inputs(batch_size, seq_length)
        cell, self.initial_state = self.build_LSTMs(batch_size, lstm_size, num_layers, keep_prob)
        outputs, self.final_state = self.run_LSTMs(num_classes, cell)
        logits, self.softmax_out = self.build_output(batch_size, seq_length, lstm_size, outputs, num_classes)
        self.loss = self.build_loss(logits, num_classes)
        self.optimizer = self.build_optimizer(learning_rate)
        
    @staticmethod
    def build_inputs(batch_size, seq_length):
        inputs = tf.placeholder(dtype=tf.int32, shape=(batch_size, seq_length), name='inputs')
        targets = tf.placeholder(dtype=tf.int32, shape=(batch_size, seq_length), name='targets')
        return inputs, targets
        
    # generate multilayer RNN cell (standard method in tensorflow)
    @staticmethod
    def lstm_gen(lstm_size, keep_prob):
        # BasicRNNCell's state and output are the same
        # BasicLSTMCell's state contains c and h. also, output is the same as h
        lstm = tf.contrib.rnn.BasicLSTMCell(num_units=lstm_size)
        drop = tf.contrib.rnn.DropoutWrapper(cell=lstm, output_keep_prob=keep_prob)
        return drop
        
    def build_LSTMs(self, batch_size, lstm_size, num_layers, keep_prob):
        cell = tf.contrib.rnn.MultiRNNCell([self.lstm_gen(lstm_size, keep_prob) for _ in range(num_layers)])
        initial_state = cell.zero_state(batch_size, dtype=tf.float32)
        return cell, initial_state
    
    def run_LSTMs(self, num_classes, cell):
        # x_one_hot.shape = (num_seqs, num_steps, num_classes)
        x_one_hot = tf.one_hot(self.inputs, num_classes)
        outputs, final_state = tf.nn.dynamic_rnn(cell, x_one_hot, initial_state=self.initial_state)
        return outputs, final_state
        
    @staticmethod
    def build_output(batch_size, seq_length, lstm_size, outputs, num_classes):
        seq_output = tf.reshape(outputs, (batch_size*seq_length, lstm_size))
        x = tf.reshape(seq_output, [-1, lstm_size])
        with tf.variable_scope('softmax'):
            softmax_w = tf.Variable(tf.truncated_normal([lstm_size, num_classes], stddev=0.1))
            softmax_b = tf.Variable(tf.zeros(num_classes))
        
        logits = tf.matmul(x, softmax_w) + softmax_b
        # properbility of each char
        softmax_out = tf.nn.softmax(logits, name='predictions')
        return logits, softmax_out
    
    def build_loss(self, logits, num_classes):
        y_one_hot = tf.one_hot(self.targets, num_classes)
        y_reshaped= tf.reshape(y_one_hot, logits.get_shape())
        
        loss = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y_reshaped)
        loss = tf.reduce_mean(loss)
        return loss

    # all the variables that can be trained
    def build_optimizer(self, learning_rate):
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.loss, tvars), 5)
        train_op = tf.train.AdamOptimizer(learning_rate)
        optimizer = train_op.apply_gradients(zip(grads, tvars))
        return optimizer
    
