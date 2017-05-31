import numpy as np
import matplotlib.pyplot as plt

x = 5 * np.random.randn(20) + 2
noise = 4 * np.random.randn(20) + 1
y = 2 * (x + noise) + 2

data = np.mat(np.vstack((x, y)))
data = data.T
meanVals = np.mean(data, axis=0)
data_centralized = data - meanVals
covMat = np.cov(data_centralized, rowvar=0)
eigVals, eigVects = np.linalg.eig(np.mat(covMat))
eigValInd = np.argsort(eigVals)
eigValInd_chosen = eigValInd[: -(1+1) : -1]
redEigVects = eigVects[:, eigValInd_chosen]
lowDDataMat = data_centralized * redEigVects
reconMat = (lowDDataMat * redEigVects.T) + meanVals

x_new = reconMat[:, 0]
y_new = reconMat[:, 1]

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'bx')
line2, = ax.plot(x_new, y_new, 'ro')
plt.show()