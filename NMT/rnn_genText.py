import time
import numpy as np
import tensorflow as tf

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

inputs = tf.placeholder(dtype=tf.int32, shape=(num_seqs, num_steps), name='inputs')
targets = tf.placeholder(dtype=tf.int32, shape=(num_seqs, num_steps), name='targets')

# generate multilayer RNN cell (standard method in tensorflow)
def lstm_gen():
    # BasicRNNCell's state and output are the same
    # BasicLSTMCell's state contains c and h, and h is the same as the output
    lstm = tf.contrib.rnn.BasicLSTMCell(num_units=lstm_size)
    drop = tf.contrib.rnn.DropoutWrapper(cell=lstm, output_keep_prob=0.5)
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
seq_output = tf.reshape(outputs, (num_seqs*num_steps, lstm_size))
x = tf.reshape(seq_output, [-1, lstm_size])
with tf.variable_scope('softmax'):
    softmax_w = tf.Variable(tf.truncated_normal([lstm_size, num_classes], stddev=0.1))
    softmax_b = tf.Variable(tf.zeros(num_classes))

logits = tf.matmul(x, softmax_w) + softmax_b
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

epochs = 20
save_every_n = 200

saver = tf.train.Saver(max_to_keep=100)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    counter = 0
    for e in range(epochs):
        new_state = sess.run(initial_state)
        # don't redefine the operator loss, it will become an int, which cannot be run by sess.run()
        # loss = 0
        for x, y in get_batches(encoded, num_seqs, num_steps):
            counter += 1
            start = time.time()
            # need to check feed new_state into initial_state is useful!
            feed = {inputs: x,
                    targets: y,
                    initial_state: new_state}
            batch_loss, new_state, _ = sess.run([loss, final_state, optimizer], feed_dict=feed)
            end = time.time()
            
            if counter % 100 == 0:
                print 'turns: {}/{}, '.format(e+1, epochs), \
                'training steps: {}, '.format(counter), \
                'error: {:.4f}, '.format(batch_loss), \
                '{:.4f} sec/batch'.format((end-start))
            if counter % save_every_n == 0:
                saver.save(sess, "checkpoints/i{}_l{}.ckpt".format(counter, lstm_size))
    
    saver.save(sess, "checkpoints/i{}_l{}.ckpt".format(counter, lstm_size))