

def cursor_proc(read_pipe, linear_mode):
  
  print("cursor control process started")

  # TODO: control the cursor

  while True:
    print("Cursor controller received " + read_pipe.readline(), end='')

