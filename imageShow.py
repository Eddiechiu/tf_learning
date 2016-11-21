import tensorflow.examples.tutorials.mnist.input_data as input_data
import numpy as np
from PIL import Image

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
x, y = mnist.train.next_batch(100)
x = np.array(x)
y = np.array(y)
M = np.zeros((280 ,280))

for i in range(100):
	for j in range(784):
		row = i / 10 * 28 + j / 28
		col = i % 10 * 28 + j % 28
		M[row, col] = x[i][j]
# pic = Image.fromarray(x*255)
# pic.show()
Image.fromarray(M*255).show()