import tensorflow as tf
import numpy as np

input_x = np.random.rand(500).astype(np.float32)
input_y = input_x * 0.5 + 0.8

W = tf.Variable(tf.random_uniform([1], -10, 10))
b = tf.Variable(tf.zeros([1]))

y = W * input_x + b

loss = tf.reduce_sum(tf.square(y - input_y))
real_loss = tf.div(loss, 100)
train = tf.train.GradientDescentOptimizer(0.01).minimize(real_loss)
init = tf.initialize_all_variables()

with tf.Session() as sess:
	sess.run(init)

	for i in range(1000):
		sess.run(train)
		if i % 100 == 0:
			print i, sess.run(W), sess.run(b)