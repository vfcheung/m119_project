from ast import literal_eval
def plotter_proc(read_pipe, linear_mode):

  print("plotter process started in {0} mode".format('linear' if linear_mode else 'angular'))
  
  # TODO: show 3d vector with matplotlib
  import numpy as np
  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D
  from matplotlib.animation import FuncAnimation
  fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

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
  x_len = 20
  ys1 = [0] * x_len
  ys2 = [0] * x_len
  ys3 = [0] * x_len
  quiver = ax.quiver(*get_arrow(0,ys1,ys2,ys3))

  ax.set_xlim(-80, 80)
  ax.set_ylim(-80, 80)
  ax.set_zlim(-80, 80)
  acceldata=literal_eval(read_pipe.readline())


  def update(theta,ys1,ys2,ys3,acceldata):
  	global quiver
    quiver.remove()

#TODO: (depends on format of data)fill in with appending accelero data
#so append will just need to change based on that.
#list of 3 numbesr
    #gives a string that represents the array

    
    

    ys1.append(acceldata[0])
    ys2.append(acceldata[1])
    ys3.append(acceldata[2])
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



    ani = FuncAnimation(fig, update, fargs=(ys1, ys2, ys3, acceldata), frames=np.linspace(0,2*np.pi,200), interval=5) #increase rate of processing by lowering interval
    plt.show() #use fargs to update for the update and append those to update the uv w?


  while True:
    print("Plotter received " + read_pipe.readline(), end='')