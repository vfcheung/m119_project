#run this from machine pc 

from multiprocessing.connection import Listener, Client


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation



x1v=0
x2v=0
x3v=0

def setx1(x1):
    x1v=x1
def setx2(x2):
    x2v=x2
def setx3(x3):
    x3v=x3

def getx1():
    return x1v
def getx2():
    return x2v
def getx3():
    return x3v




def get_arrow(theta,ys1,ys2,ys3):
    accelero=[1,23,10]
    accelero1=[-100,-23,-10]
   # x = np.cos(theta)
#The x, y and z coordinates of the arrow locations (default is tail of arrow; see pivot kwarg)

#u can change these x y z vvaules and spin them based on theta if u want but i just froze it...

    x=np.cos(accelero1[0])
    y=np.cos(accelero1[1])
    z=np.cos(accelero1[2])
    #y = np.sin(theta)
    #z = 0
    u = ys1#np.sin(2*theta)
    v = ys2#np.sin(3*theta)
    w = ys3#np.cos(3*theta)
    return x,y,z,u,v,w


def update(theta,ys1,ys2,ys3):
    global quiver
    quiver.remove()

#TODO: (depends on format of data)fill in with appending accelero data
#so append will just need to change based on that.
    
    


    ys1.append(getx1())
    ys2.append(getx2())
    ys3.append(getx3())
    quiver = ax.quiver(*get_arrow(theta,ys1,ys2,ys3)) 
    # Limit x and y lists to 200 samples - 2s 
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]
    ys3 = ys3[-x_len:]

    # Draw dis and accel lists
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)
    line3.set_ydata(ys3)

    return line1,line2,line3,



serv = Listener(('',5005))
client = serv.accept()
cli = Client(('localhost', 5000))


while True:
    if (client.poll(0)):
        acceldata = client.recv()

        print("Received data: ", acceldata)
        parsed_msg = msg.split(",")
        setx1(int(parsed_msg[0]))
        setx2(int(parsed_msg[1]))
        setx3(int(parsed_msg[2]))

        cli.send(acceldata)

        x_len = 20
        ys1 = [0] * x_len
        ys2 = [0] * x_len
        ys3 = [0] * x_len

#create fig
        fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
#quiver
        quiver = ax.quiver(*get_arrow(0,ys1,ys2,ys3))
#params
        ax.set_xlim(-80, 80)
        ax.set_ylim(-80, 80)
        ax.set_zlim(-80, 80)
        ani = FuncAnimation(fig, update, fargs=(ys1, ys2, ys3), frames=np.linspace(0,2*np.pi,200), interval=5) #increase rate of processing by lowering interval
        plt.show() #use fargs to update for the update and append those to update the uv w?


