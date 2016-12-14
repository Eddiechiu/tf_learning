import numpy as np 
import random
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

x = np.arange(1, 300, 1)
y = 10 * 1e-6 * (pow((x / 300),  39) + random.random())

ax = plt.subplot(111)

line1 = ax.plot(x, y, '--', )
plt.ylabel('U / (V)')
plt.xlabel('I / (A)')
# use a tuple to wirte the legend content that it can be shown completely
ax.legend(line1, ('Critical Current', ), loc='upper left') 

plt.show()