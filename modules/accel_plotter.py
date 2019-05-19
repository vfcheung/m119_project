

def plotter_proc(read_pipe, linear_mode):

  print("plotter process started in {0} mode".format('linear' if linear_mode else 'angular'))
  
  # TODO: show 3d vector with matplotlib

  while True:
    print("Plotter received " + read_pipe.readline(), end='')
