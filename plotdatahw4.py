#!/usr/bin/python
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import hexiwearserial
import sys

#  Serial setup according to command line arguments
python_version = sys.version[0]
if len(sys.argv) != 2:
    print ("Wrong Number of Arguments!")
    print ("Please use format: python plotdatahw4.py SerialAddress")
else:
    address = sys.argv[1]
    if python_version == "2":
        python3 = False
    else:
        python3 = True

baud_rate = 9600
timeout = 2

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.title('hw4 Project')
#ax2 = fig.add_subplot(312)
#ax3=fig.add_subplot(313)
ax1.set(ylabel='Accelerationx (mg)')
#ax2.set(ylabel='Accelerationy (mg)')
#ax3.set(ylabel='Accelerationz (mg)')

# plot parameters
x_len = 200
accel1_range = [-1000, 1000]
#accel2_range = [-450, 450]
#accel3_range = [-450, 450]
xs = list(range(0, 200))
ys1 = [0] * x_len
#ys2 = [0] * x_len
#ys3 = [0] * x_len

ax1.set_ylim(accel1_range)
line1, = ax1.plot(xs, ys1, animated=True)
#ax2.set_ylim(accel2_range)
#line2, = ax2.plot(xs, ys2, animated=True)
#ax3.set_ylim(accel3_range)
#line3, = ax3.plot(xs, ys3, animated=True)

# serial initialization
hexiwear = hexiwearserial.hexiwearserial(address, baud_rate, timeout, python3)
hexiwear.init_connection()
#sensortile.collect_data(numofruns)

# This function is called periodically from FuncAnimation
# def animate(i, xs, ys):
def animate(i, ys1):

    # get displacement, acceleration
    accelx = hexiwear.collect_data()

    # Add dis and accel to lists
    ys1.append(accelx)
    #ys2.append(accely)
    #ys3.append(accelz)

    # Limit x and y lists to 200 samples - 2s 
    ys1 = ys1[-x_len:]
   # ys2 = ys2[-x_len:]
   # ys3 = ys3[-x_len:]

    # Draw dis and accel lists
    line1.set_ydata(ys1)
    #line2.set_ydata(ys2)
    #line3.set_ydata(ys3)

    return line1,#, line2, line3


# Set up plot to call animate() function periodically
# interval = 10ms
ani = animation.FuncAnimation(fig, animate, fargs=(ys1,), interval=3, blit=True)
plt.show()

# shutdown the system after closing the plot
hexiwear.close_connection()