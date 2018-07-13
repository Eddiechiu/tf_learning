# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 00:58:38 2018

@author: derong
"""
#%%
import tensorflow as tf
import numpy as np
from CharNet import CharNet

with open('anna.txt', 'r') as f:
    text = f.read()

vocab = set(text)
vocab_to_int = {c: i for i, c in enumerate(vocab)}
int_to_vocab = {i: c for i, c in enumerate(vocab)}

#%%
num_seqs = 20
# steps in each seq
num_steps = 100
# num of neru in each lstm
lstm_size = 128
num_classes = 84
learning_rate = 0.001
charNet = CharNet(batch_size=num_seqs, seq_length=num_steps,
                  lstm_size=lstm_size, keep_prob=0.5, num_classes=num_classes,
                  num_layers=3, learning_rate=0.001, training=False)

#%%
def pick_top_n(preds, vocab_size, top_n=5):
    p = np.squeeze(preds)
    p[np.argsort(p)[:-top_n]] = 0
    p = p / np.sum(p)
    c = np.random.choice(vocab_size, 1, p=p)[0]
    return c
    
def sample(checkpoint, n_samples, lstm_size, vocab_size, prime="The best"):

    samples = [c for c in prime]
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, checkpoint)
        new_state = sess.run(charNet.initial_state)
        for c in prime:
            x = np.zeros((1, 1))
            x[0,0] = vocab_to_int[c]
            feed = {charNet.inputs: x,
                    charNet.initial_state: new_state}
            preds, new_state = sess.run([charNet.softmax_out, charNet.final_state], feed_dict=feed)

        c = pick_top_n(preds, len(vocab))
        samples.append(int_to_vocab[c])
        
        for i in range(n_samples):
            x[0,0] = c
            feed = {charNet.inputs: x,
                    charNet.initial_state: new_state}
            preds, new_state = sess.run([charNet.softmax_out, charNet.final_state], feed_dict=feed)

            c = pick_top_n(preds, len(vocab))
            samples.append(int_to_vocab[c])
        
    return ''.join(samples)

checkpoint = tf.train.latest_checkpoint('checkpoints')
samp = sample(checkpoint, 2000, lstm_size, len(vocab), prime="The")
print(samp)