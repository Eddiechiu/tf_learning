import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

data = pd.read_csv('10 A.csv', skiprows=15, usecols=[1, 2])
data.columns=['U', 'I']
data.I = data.I * 1000
time = np.linspace(0, 0.15, 10010)

fig = plt.figure()
ax1 = fig.add_subplot(111)
line1, = ax1.plot(time, data.U, color='b', linestyle='--', label='voltage')
ax1.set_title('Voltage vs. Current')
ax1.set_ylabel('Voltage / V')

ax2 = ax1.twinx()
line2, = ax2.plot(time, data.I, color='r', label='current')
ax2.set_ylabel('Current / A')
ax2.set_xlabel('Time / s')
plt.legend(loc=0, handles=[line1, line2])
plt.show()

# plt.title('Voltage vs. Current')
# plt.xlabel('time / s')
# plt.ylabel('Voltage / V')
# plt.twinx()
# plt.ylabel('Current / A')
# line1 = plt.plot(time, data.U, color='red', linestyle='--', label='voltage')
# line2 = plt.plot(time, data.I, color='blue', label='current')
# plt.legend(loc=0)
# plt.grid(True)
# plt.show()