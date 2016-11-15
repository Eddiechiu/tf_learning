import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)


#### Step 1: variables defination and output calculation
# input x data
x = tf.placeholder(tf.float32, [None, 784])
# acctual y data
y_real = tf.placeholder(tf.float32, [None, 10])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10])+0.1)

# output data calculated
y_pre = tf.nn.softmax(tf.matmul(x, W) + b)


#### Step 2: loss calculation and train step 
# reduce_sum(...) means the total sum of the tensor ...
# the cross_entropy funcion or loss function depends on the activation function, in this case, it's softmax
cross_entropy = -tf.reduce_sum(y_real * tf.log(y_pre))

train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cross_entropy)


#### Step 3: variables initialization
init = tf.initialize_all_variables()
# the train process should be put into a container, called Session
sess = tf.Session()
sess.run(init)


#### Step 4: iterative training
for i in range(1000):
	batch_xs, batch_ys = mnist.train.next_batch(100)
	sess.run(train_step, feed_dict={x: batch_xs, y_real: batch_ys})

	if (i+1) % 50 == 0: 
		# argmax returns the index of the max value along Direction=1
		# function 'cast' turns correction_prediction from int to tf.float32 
		accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_real, 1), tf.argmax(y_pre, 1)), tf.float32))
		print 'step: ', i+1, '  accuracy: ', sess.run(accuracy, feed_dict={x: mnist.test.images, y_real: mnist.test.labels})