from __future__ import print_function
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

with tf.name_scope('Input'):
	x = tf.placeholder(tf.float32, [None, 784], name='input')
	y_real = tf.placeholder(tf.float32, [None, 10], name='output')
	keep_prob = tf.placeholder(tf.float32)
	x_image = tf.reshape(x, [-1,28,28,1])

def weight_init(shape):
	init = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(init)

def bias_init(shape):
	init = tf.constant(0.1, shape=shape)
	return tf.Variable(init)

def conv2d(x, W):
	# strides=[1, x_movement, y_movement, 1], in which strides[0] and strides[3] must be equal to 1.
	return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

W_conv1 = weight_init([5,5,1,8]) # patch 5x5, input size 1, output size 32 (which means we use 32 maps to convolute the original picture).
b_conv1 = bias_init([8])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1) # size is 28x28x32
h_pool1 = max_pool_2x2(h_conv1)  # size is 14x14x32

W_conv2 = weight_init([5,5,8,32])
b_conv2 = bias_init([32])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) # size is 14x14x64
h_pool2 = max_pool_2x2(h_conv2)  # size is 7x7x64

W_f1 = weight_init([7*7*32, 256])
b_f1 = bias_init([256])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_f1) + b_f1)
h_fc_drop = tf.nn.dropout(h_fc1, keep_prob)

W_f2 = weight_init([256, 10])
b_f2 = bias_init([10])
pred = tf.nn.softmax(tf.matmul(h_fc_drop, W_f2) + b_f2)

cross_entropy = tf.reduce_mean(-y_real * tf.log(pred))
train = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())

	for i in range(3000):
		batch_xs, batch_ys = mnist.train.next_batch(100)
		sess.run(train, feed_dict={x: batch_xs, y_real: batch_ys, keep_prob: 0.5})

		if (i+1) % 500 == 0: 
			# argmax returns the index of the max value along Direction=1
			# function 'cast' turns correction_prediction from int to tf.float32 
			accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_real, 1), tf.argmax(pred, 1)), tf.float32))
			print('step: ', i+1, '  accuracy: ', sess.run(accuracy, feed_dict={x: mnist.test.images, y_real: mnist.test.labels, keep_prob: 1}))

# time consumed:686 s, accuracy: ~97.2%
        