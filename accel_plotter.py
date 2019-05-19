

def plotter_proc(read_pipe):

  print("plotter process started")
  
  # TODO: show 3d vector with matplotlib

  while True:
    print(read_pipe.readline(), end='')
    
