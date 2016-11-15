import numpy as np

X = np.array([[1,2,3],
	          [4,5,6]])

print 'X.shape: \n', X.shape, '\n'

print 'X[:]: \n', X[:], '\n'

print 'X[:, np.newaxis]: \n', X[:, np.newaxis].shape, '\n'

print 'X[np.newaxis, :]: \n',X[np.newaxis, :].shape, '\n'

print X[:, np.newaxis] + X[np.newaxis, :], '\n'

print np.array([[[1,2,3]],[[4,5,6]]]).shape

print np.array([[[1,2,3],[4,5,6]]]).shape