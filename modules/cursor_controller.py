from ast import literal_eval
from pymouse import PyMouse
import numpy as np

from transfer_functions import trapezoidal_integrate as trap_int


def angular_transfer_function(x, y, z):
  # TODO
  mouse_x = 3 * x
  mouse_y = 3 * y
  return mouse_x, mouse_y


def linear_transfer_function(raw_data,previous_data,mouse_pos):
  # TODO
  (mouse_x,mouse_y) = trap_int(mouse_pos,raw_data,previous_data)
  
  return mouse_x, mouse_y


def cursor_proc(read_pipe, linear_mode):

  print("cursor control process started in {0} mode".format('linear' if linear_mode else 'angular'))

  global x_dim
  global y_dim

  m = PyMouse()
  x_dim, y_dim = m.screen_size()

  previous_data = (0,0)

  while True:
    raw_data = literal_eval(read_pipe.readline())
    if linear_mode:
      mouse_pos = linear_transfer_function(raw_data,previous_data,mouse_pos)
    else:
      mouse_pos = angular_transfer_function(*raw_data)
    m.move(*mouse_pos)

