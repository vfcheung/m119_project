def plotter_proc(cli, read_pipe, linear_mode):

  print("plotter process started in {0} mode".format('linear' if linear_mode else 'angular'))
  
  # TODO: show 3d vector with matplotlib
  #cli.send("{},{}".format(dev,val))
  #sending it via tcp now.

  while True:
    #print("Plotter received " + read_pipe.readline(), end='')
    #only do this line when we need to plot stuff.
    cli.send("{}".format(read_pipe.readline()))
