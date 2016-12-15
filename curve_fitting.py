import numpy as np 
import random
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

x = np.linspace(250, 300, 100)
noize = np.random.random([100])
y = 1e-5 * pow((x / 300),  39) + 4e-7 * (2 * noize - 1)

# define the function used to fit the curve
def func(x, a, b, c, d):
	return a * pow((x / b),  c) + d

# 'bounds' limits the parameters' range; 'method' can be chosen from ['lm', 'trf', 'dogbox'] 
params, pcov = curve_fit(func, x, y, bounds=([0, 280, 30, -1e-6], [5e-5, 320, 45, 1e-6]), method='dogbox')
y_cal = func(x, params[0], params[1], params[2], params[3])

ax = plt.subplot(111)
line1 = ax.plot(x, y, 'ro', label='Exp val')
line2 = ax.plot(x, y_cal, 'b--', label='Fit val')
plt.ylabel('U / (V)')
plt.xlabel('I / (A)')
# # use a tuple to wirte the legend content that it can be shown completely
# ax.legend(line1, ('Exp val', ), loc='upper left') 

handles, labels = ax.get_legend_handles_labels()

ax.legend(handles[::-1], labels[::-1], loc='upper left')

params_name = ['lambda', 'Ic', 'n_value', 'bias']

plt.show()
for i in range(len(params_name)):
	print(params_name[i], ' = ', params[i])

for i in handles:
	print(i)