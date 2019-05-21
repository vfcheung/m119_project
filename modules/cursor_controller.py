from ast import literal_eval
from pymouse import PyMouse
import numpy as np

from modules import transfer_functions as tf


def angular_transfer_function(x, y, z):
  # TODO
  mouse_x = 3 * x
  mouse_y = 3 * y
  return mouse_x, mouse_y


def linear_transfer_function(raw_data,previous_acc,previous_vel,mouse_pos):
  new_acc = (raw_data[0],raw_data[1])
  prev_acc = (previous_acc[0],previous_acc[1])
  '''
  prev_vel = (previous_vel[0],previous_vel[1])
  mouse_vel_x,mouse_vel_y = tf.trapezoidal_integrate(prev_vel,new_acc,prev_acc)
  new_vel = (mouse_vel_x, mouse_vel_y)
  mouse_pos_x, mouse_pos_y = tf.trapezoidal_integrate(mouse_pos,new_vel,prev_vel)
  '''
  mouse_pos_x, mouse_pos_y = tf.trapezoidal_integrate(mouse_pos,new_acc,prev_acc)
  return mouse_pos_x, mouse_pos_y


def cursor_proc(read_pipe, linear_mode):

  print("cursor control process started in {0} mode".format('linear' if linear_mode else 'angular'))

  global x_dim
  global y_dim

  m = PyMouse()
  x_dim, y_dim = m.screen_size()

  previous_acc = (0,0,0)
  previous_vel = (0,0,0)
  mouse_pos = (0,0)

  while True:
    raw_data = literal_eval(read_pipe.readline())
    if linear_mode:
      '''
      print("Doing linear transfer function")
      mouse_pos_x, mouse_pos_y, mouse_vel_x, mouse_vel_y  = linear_transfer_function(raw_data,previous_acc,previous_vel,mouse_pos)
      print("New mouse pos: ",mouse_pos)
      previous_acc = raw_data
      previous_vel = (mouse_vel_x,mouse_vel_y,0)
      '''
      mouse_pos_x, mouse_pos_y = linear_transfer_function(raw_data,previous_acc,previous_vel,mouse_pos)
      mouse_pos = (int(mouse_pos_x),int(mouse_pos_y))
    else:
      mouse_pos = angular_transfer_function(*raw_data)
    m.move(*mouse_pos)

