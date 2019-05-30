from ast import literal_eval
from pymouse import PyMouse
import numpy as np

from modules import transfer_functions as tf
from modules import filter_data as fdata

def angular_transfer_function(x, y, z):
  # TODO
  mouse_x = 3 * x
  mouse_y = 3 * y
  return mouse_x, mouse_y


def linear_transfer_function(raw_data,previous_acc,previous_vel,mouse_pos,mode="orientation"):
  if mode == "once":
    mouse_pos_x, mouse_pos_y = tf.integrate_1_tf(raw_data,previous_acc,mouse_pos)
    return mouse_pos_x, mouse_pos_y
  elif mode == "twice":
    mouse_pos_x, mouse_pos_y, mouse_vel_x, mouse_vel_y = tf.integrate_2_tf(raw_data,previous_acc,previous_vel,mouse_pos)
    # Check cursor velocity
    if mouse_vel_x > 30:
      mouse_vel_x = 30
    if mouse_vel_x < -30:
      mouse_vel_x = -30
    if mouse_vel_y > 30:
      mouse_vel_y = 30
    if mouse_vel_y < -30:
      mouse_vel_y = -30
    return mouse_pos_x, mouse_pos_y, mouse_vel_x, mouse_vel_y
  elif mode == "orientation":
    mouse_pos_x, mouse_pos_y = tf.orientation_tf(raw_data)
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

  # Transfer function modes
  #   Orientation: Maps absolute orientation to cursor
  #   Once: Integrates accel data once
  #   Twice: Integrates accel data twice, currently very bad
  tf_mode = "orientation"
  # CD gain: a scaling factor for the cursor position, only useful for integration modes
  cd_gain = 1

  while True:
    raw_data = literal_eval(read_pipe.readline())
    #print("raw data : ",raw_data)
    #print("prev data: ", previous_acc)
    #raw_data = fdata.filter(raw_data, previous_acc, 0.6) #apply filter
    #print("filtered data : ",raw_data)
    if linear_mode:
      tf_out = linear_transfer_function(raw_data,previous_acc,previous_vel,mouse_pos,mode="orientation")
      previous_acc=raw_data
      if tf_mode == "orientation" or tf_mode == "once":
        mouse_pos_x = tf_out[0]
        mouse_pos_y = tf_out[1]
      elif tf_mode == "twice":
        mouse_pos_x = tf_out[0]
        mouse_pos_y = tf_out[1]
        mouse_vel_x = tf_out[2]
        mouse_vel_y = tf_out[3]
        previous_vel = (mouse_vel_x,mouse_vel_y,0)

      move_pos_x = cd_gain*mouse_pos_x
      move_pos_y = cd_gain*mouse_pos_y

      # Check screen edge
      if move_pos_x > x_dim:
        move_pos_x = x_dim
      if move_pos_x < 0:
        mouse_pos_x = 0
      if move_pos_y > y_dim:
        move_pos_y = y_dim
      if move_pos_y < 0:
        move_pos_y = 0

      pos_to_move = (int(move_pos_x),int(move_pos_y))
      print("New mouse pos: ", pos_to_move)
      mouse_pos = (mouse_pos_x,mouse_pos_y)
      previous_acc = raw_data
      
    else:
      pos_to_move = angular_transfer_function(*raw_data)
    m.move(*pos_to_move)
