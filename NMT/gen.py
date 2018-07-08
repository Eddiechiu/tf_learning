# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 00:58:38 2018

@author: derong
"""
#%%
import tensorflow as tf
import numpy as np

with open('anna.txt', 'r') as f:
    text = f.read()

vocab = set(text)
vocab_to_int = {c: i for i, c in enumerate(vocab)}
int_to_vocab = {i: c for i, c in enumerate(vocab)}

#%%
# num of seqs in each batch
num_seqs = 1
# steps in each seq
num_steps = 1
# num of neru in each lstm
lstm_size = 128
num_classes = len(vocab)
learning_rate = 0.001

inputs = tf.placeholder(dtype=tf.int32, shape=(num_seqs, num_steps), name='inputs')
targets = tf.placeholder(dtype=tf.int32, shape=(num_seqs, num_steps), name='targets')

# generate multilayer RNN cell (standard method in tensorflow)
def lstm_gen():
    # BasicRNNCell's state and output are the same
    # BasicLSTMCell's state contains c and h
    lstm = tf.contrib.rnn.BasicLSTMCell(num_units=lstm_size)
    drop = tf.contrib.rnn.DropoutWrapper(cell=lstm, output_keep_prob=1)
    return drop
cell = tf.contrib.rnn.MultiRNNCell([lstm_gen() for _ in range(3)])

initial_state = cell.zero_state(num_seqs, dtype=tf.float32)

# x_one_hot.shape = (num_seqs, num_steps, num_classes)
x_one_hot = tf.one_hot(inputs, num_classes)


#%%
outputs, state = tf.nn.dynamic_rnn(cell, x_one_hot, initial_state=initial_state)
final_state = state

# don't know why tf.concat doesn't work
# seq_output = tf.concat(outputs, axis=1)
xx = tf.reshape(outputs, [-1, lstm_size])
with tf.variable_scope('softmax'):
    softmax_w = tf.Variable(tf.truncated_normal([lstm_size, num_classes], stddev=0.1))
    softmax_b = tf.Variable(tf.zeros(num_classes))

logits = tf.matmul(xx, softmax_w) + softmax_b
# properbility of each char
out = tf.nn.softmax(logits, name='predictions')


y_one_hot = tf.one_hot(targets, num_classes)
y_reshaped= tf.reshape(y_one_hot, logits.get_shape())

loss = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y_reshaped)
loss = tf.reduce_mean(loss)

#%%
# all the variables that can be trained
tvars = tf.trainable_variables()
grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tvars), 5)
train_op = tf.train.AdamOptimizer(learning_rate)
optimizer = train_op.apply_gradients(zip(grads, tvars))


#%%
def pick_top_n(preds, vocab_size, top_n=5):
    p = np.squeeze(preds)
    p = np.squeeze(preds)
    p[np.argsort(p)[:-top_n]] = 0
    p = p / np.sum(p)
    c = np.random.choice(vocab_size, 1, p=p)[0]
    return c
    
def sample(checkpoint, n_samples, lstm_size, vocab_size, prime="The "):

    samples = [c for c in prime]
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, checkpoint)
        new_state = sess.run(initial_state)
        for c in prime:
            x = np.zeros((1, 1))
            x[0,0] = vocab_to_int[c]
            feed = {inputs: x,
                    initial_state: new_state}
            preds, new_state = sess.run([out, final_state], feed_dict=feed)

        c = pick_top_n(preds, len(vocab))
        samples.append(int_to_vocab[c])
        
        for i in range(n_samples):
            x[0,0] = c
            feed = {inputs: x,
                    initial_state: new_state}
            preds, new_state = sess.run([out, final_state], feed_dict=feed)

            c = pick_top_n(preds, len(vocab))
            samples.append(int_to_vocab[c])
        
    return ''.join(samples)

checkpoint = tf.train.latest_checkpoint('checkpoints')
samp = sample(checkpoint, 2000, lstm_size, len(vocab), prime="The")
print(samp)