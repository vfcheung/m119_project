# Import for multiprocessing server
from multiprocessing.connection import Listener

#import for plotting acceleration data
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#x1v=0
#x2v=0

serv = Listener(('',5000))
client = serv.accept()

'''
def setx1(x1):
    x1v=x1
def setx2(x2):
    x2v=x2

def getx1():
    return x1v
def getx2():
    return x2v
'''

def animate(i, ys1, ys2):
    if (client.poll(0)):
    	msg = client.recv()
    	parsed_msg = msg.split(",")
    	if parsed_msg[0] == "1":
    		ys1.append(float(parsed_msg[1])/80)
    	elif parsed_msg[0] == "2":
    		ys2.append(float(parsed_msg[1])/80)
    	print("Received data: ", msg)
    	print("device: ", parsed_msg[0])
    else:
    	ys1.append(ys1[-1])
    	ys2.append(ys2[-1])

    # Limit x and y lists to 200 samples - 2s 
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]

    # Draw dis and accel lists
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)

    return line1, line2,

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(211)
plt.title('hw4 Project animated plot')
ax2 = fig.add_subplot(212)
ax1.set(ylabel='Acceleration1 (g)')
ax2.set(ylabel='Acceleration2 (g)')

# plot parameters
x_len = 200
accel1_range = [-1.5, 1.5]
accel2_range = [-1.5, 1.5]
xs = list(range(0, 200))
ys1 = [0.0] * x_len
ys2 = [0.0] * x_len
ax1.set_ylim(accel1_range)
line1, = ax1.plot(xs, ys1, animated=True)
ax2.set_ylim(accel2_range)
line2, = ax2.plot(xs, ys2, animated=True)
ani = animation.FuncAnimation(fig, animate, fargs=(ys1, ys2), interval=3, blit=True)
plt.show()