

def plotter_proc(read_pipe, linear_mode):

  print("plotter process started")
  
  # TODO: show 3d vector with matplotlib

  while True:
    print("Plotter received " + read_pipe.readline(), end='')
