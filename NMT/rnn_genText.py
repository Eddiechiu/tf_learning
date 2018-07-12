import time
import numpy as np
import tensorflow as tf
from CharNet import CharNet

#%%
tf.reset_default_graph()

#%%
with open('anna.txt', 'r') as f:
    text = f.read()

vocab = set(text)
vocab_to_int = {c: i for i, c in enumerate(vocab)}
int_to_vocab = {i: c for i, c in enumerate(vocab)}

encoded = np.array([vocab_to_int[c] for c in text], dtype=np.int32)

#%%
def get_batches(arr, n_seqs, n_steps):
    batch_size = n_seqs * n_steps
    n_batches = int(len(arr) / batch_size)

    arr = arr[: batch_size * n_batches]

    arr = arr.reshape((n_seqs, -1))

    for n in range(0, arr.shape[1], n_steps):
        x = arr[:, n:n+n_steps]
        y = np.zeros_like(x)
        y[:, :-1], y[:, -1] = x[:, 1:], x[:, 0]
        yield x, y


#%%
#batches = get_batches(encoded, 1, 50)
#
#x, y = next(batches)
#
#print 'x\n', x[:10, :10]

#%%
# num of seqs in each batch, or it is called batch_size
num_seqs = 20
# steps in each seq
num_steps = 100
# num of neru in each lstm
lstm_size = 128
num_classes = len(vocab)
learning_rate = 0.001

charNet = CharNet(batch_size=num_seqs, seq_length=num_steps,
                  lstm_size=lstm_size, keep_prob=0.5, num_classes=num_classes,
                  num_layers=2, learning_rate=0.001, training=True)

epochs = 20
save_every_n = 200

saver = tf.train.Saver(max_to_keep=100)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    counter = 0
    for e in range(epochs):
        new_state = sess.run(charNet.initial_state)
        # don't redefine the operator loss, it will become an int, which cannot be run by sess.run()
        # loss = 0
        for x, y in get_batches(encoded, num_seqs, num_steps):
            counter += 1
            start = time.time()
            # need to check feed new_state into initial_state is useful!
            feed = {charNet.inputs: x,
                    charNet.targets: y,
                    charNet.initial_state: new_state}
            batch_loss, new_state, _ = sess.run([charNet.loss,
                                                 charNet.final_state,
                                                 charNet.optimizer],
                                                 feed_dict=feed)
            end = time.time()
            
            if counter % 100 == 0:
                print 'turns: {}/{}, '.format(e+1, epochs), \
                'training steps: {}, '.format(counter), \
                'error: {:.4f}, '.format(batch_loss), \
                '{:.4f} sec/batch'.format((end-start))
            if counter % save_every_n == 0:
                saver.save(sess, "checkpoints/i{}_l{}.ckpt".format(counter, lstm_size))
    
    saver.save(sess, "checkpoints/i{}_l{}.ckpt".format(counter, lstm_size))