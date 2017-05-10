import numpy as np 
import matplotlib.pyplot as plt 

x = np.linspace(0, 1, 100)
radom = 0.04 * np.random.randn(100)
y = 3 * x + 0.1 * np.sin(50 * x) + radom

x_1 = np.ones((100, 1))
x_2 = np.mat(x).T
X_data = np.hstack((x_1, x_2)) # merge two matrices in horizontal direction
Y_data = np.mat(y).T

print(X_data[0,:])

def lwlr(testPoint, xMat, yMat, k=0.1):
	weights = np.mat(np.eye(100))
	for j in range(100):
		diffMat = testPoint - xMat[j, :]
		weights[j, j] = np.exp(diffMat * diffMat.T / (-2.0 * k ** 2))
		xTx = xMat.T * (weights * xMat)
	if np.linalg.det(xTx) == 0.0:
		print('This matrix is singular and there is no solution')
	ws = xTx.I * (xMat.T * (weights * yMat))
	
	return testPoint * ws

def lwlrTest(testMat, xMat, yMat, k=0.1):
	yHat = np.zeros(100)
	for i in range(100):
		yHat[i] = lwlr(testMat[i], xMat, yMat, k)
	return yHat

Y_pre = lwlrTest(X_data, X_data, Y_data, k=0.01)
print(np.shape(Y_pre))
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, Y_pre, 'r')
line2, = ax.plot(x, y, 'b.')
plt.show()