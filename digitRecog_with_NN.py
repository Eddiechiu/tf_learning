import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

with tf.name_scope('Input'):
	x = tf.placeholder(tf.float32, [None, 784], name='x_input')
	y_real = tf.placeholder(tf.float32, [None, 10], name='y_input')

with tf.name_scope('Weights'):
	Weights = {
		'h1': tf.Variable(tf.random_normal([784, 256]), name='W_1'),
		'h2': tf.Variable(tf.random_normal([256, 256]), name='W_2'),
		'out': tf.Variable(tf.random_normal([256, 10]), name='W_3'),
	}
	with tf.name_scope('biases'):
		biases = {
			'h1': tf.Variable(tf.random_normal([256]), name='b_1'),
			'h2': tf.Variable(tf.random_normal([256]), name='b_2'),
			'out': tf.Variable(tf.random_normal([10]), name='b_3'),
		}

with tf.name_scope('Layer1'):
	layer1_raw = tf.add(tf.matmul(x, Weights['h1']), biases['h1'])
	layer1 = tf.nn.relu(layer1_raw, name='output_layer1')

	tf.histogram_summary('W_1', Weights['h1'])
	tf.histogram_summary('b_1', biases['h1'])

with tf.name_scope('Layer2'):
	layer2_raw = tf.add(tf.matmul(layer1, Weights['h2']), biases['h2'])
	layer2 = tf.nn.relu(layer2_raw, name='output_layer1')

	tf.histogram_summary('W_2', Weights['h2'])
	tf.histogram_summary('b_2', biases['h2'])

with tf.name_scope('Layer3'):
	output = tf.add(tf.matmul(layer2, Weights['out']), biases['out'], name='output_final')

	tf.histogram_summary('W_3', Weights['out'])
	tf.histogram_summary('b_3', biases['out'])

with tf.name_scope('loss'):
	loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, y_real))
	tf.scalar_summary('loss', loss)

train = tf.train.AdamOptimizer(0.01).minimize(loss)

init = tf.initialize_all_variables()

with tf.Session() as sess:
	merged = tf.merge_all_summaries()
	writer = tf.train.SummaryWriter('test/', sess.graph)
	sess.run(init)

	for i in range(1, 1000):
		x_batch, y_batch = mnist.train.next_batch(100)
		sess.run(train, feed_dict={x: x_batch, y_real: y_batch})
		result = sess.run(merged, feed_dict={x: x_batch, y_real: y_batch})
		# writer.add_summary(result, i)
		acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_real, 1), tf.argmax(output, 1)), tf.float32))
		print 'step: ', i, ' accuracy: ', acc.eval({x: mnist.test.images, y_real: mnist.test.labels})


# operation time ~ 3 hours, accuracy ~94.5%