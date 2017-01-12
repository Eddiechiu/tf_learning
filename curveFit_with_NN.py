import tensorflow as tf 
import numpy as np
import matplotlib.pyplot as plt

# create a layer and return the output
def add_layer(input, input_size, output_size, n_layer, activation_func=None):
	layer_name = 'Layer%s' % n_layer
	# tf.name_scope is to name and define this operation in tensorboard graph
	with tf.name_scope(layer_name):
		with tf.name_scope('Weights'):
			W = tf.Variable(tf.random_normal([input_size, output_size]), name='W')
			# use histogram to summarize the W and b
			tf.histogram_summary(layer_name + '/Weights', W)
		with tf.name_scope('bias'):
			b = tf.Variable(tf.zeros([1, output_size]) + 0.1, name='bias')
			tf.histogram_summary(layer_name + '/bias', b)
		with tf.name_scope('Wx_plus_b'):
			Wx_plus_b= tf.matmul(input, W) + b
		if activation_func:
			output = activation_func(Wx_plus_b)
		else:
			output = Wx_plus_b
		tf.histogram_summary(layer_name + '/output', output)
		return output

# create the training data
# trun a (1000,) array to a 1000x1 matrix, notify the difference between an array and a 1xn matrix
x_data = np.linspace(-1, 1, 500)[:, np.newaxis]
noise = 2 * np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

# plt.figure(figsize=(8, 4))
# plt.plot(x_data, y_data)
# plt.show()
with tf.name_scope('input'):
	xs = tf.placeholder(tf.float32, [None, 1], name='input_x')
	ys = tf.placeholder(tf.float32, [None, 1], name='input_y')

layer_1 = add_layer(xs, 1, 10, 1, tf.nn.relu)
layer_2 = add_layer(layer_1, 10, 1, 2)
with tf.name_scope('loss'):
	loss = tf.reduce_mean(tf.square(layer_2 - ys), name='loss')
	# loss is a scalar, so it is different from summarize W and b
	tf.scalar_summary('loss', loss)
with tf.name_scope('Train'):
	train = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

init = tf.initialize_all_variables()

print('training started')

with tf.Session() as sess:
	merged = tf.merge_all_summaries()
	# create the tensorboard
	writer = tf.train.SummaryWriter('Documents/', sess.graph)
	
	sess.run(init)
	
	# create a figure to show the fitting process
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	# 
	ax.scatter(x_data, y_data)
	# start the figure, notify that .show() can also start the figure, but it will pause the program
	# so .ion() is better 
	plt.ion()

	for i in range(1000):

		# feed training data into the model(graph)
		sess.run(train, feed_dict={xs: x_data, ys: y_data})
		if i % 10 == 0:
			result = sess.run(merged, feed_dict={xs: x_data, ys: y_data})
			writer.add_summary(result, i)
			try:
				# remove the former fitting line in the figure, then a dynamic process is shown.
				# the object line is greated below
				ax.lines.remove(line[0])
			except Exception:
				pass
			# print sess.run(loss, feed_dict={xs: x_data, ys: y_data})

			# the output of layer_2 is calculated from x_data, the its value should be feeded
			prediction_value = sess.run(layer_2, feed_dict={xs: x_data})
			line = ax.plot(x_data, prediction_value, 'r-', lw=5)
			plt.pause(0.1)

print('training finished')
