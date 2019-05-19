import errno, sys, os
from argparse import ArgumentParser

from modules.ble_server import server_proc
from modules.accel_plotter import plotter_proc
from modules.cursor_controller import cursor_proc


mac_addresses = {
  'vincent': '00:3B:40:0B:00:0E',
  'jingbin': '00:09:50:04:00:32',
  'justin': '00:26:50:04:00:30'
}


def main():

  parser = ArgumentParser()
  parser.add_argument('device', help='vincent, jingbin, or justin')
  parser.add_argument('--linear', help='switch to linear mode', action='store_true')
  args = parser.parse_args()

  if args.device not in mac_addresses:
    sys.stderr.write('choose device vincent, jingbin, or justin\n')
    sys.exit(errno.errorcode[errno.EINVAL])

  mac_address = mac_addresses[args.device]

  plotter_pipe = os.pipe()
  plotter_fds = [os.fdopen(plotter_pipe[0],'r'), os.fdopen(plotter_pipe[1],'w')]
  pid1 = os.fork()
  if pid1:
    cursor_pipe = os.pipe()
    cursor_fds = [os.fdopen(cursor_pipe[0],'r'), os.fdopen(cursor_pipe[1],'w')]
    pid2 = os.fork()
    if pid2:
      # BLE server process
      plotter_fds[0].close()
      cursor_fds[0].close()
      server_proc(plotter_fds[1], cursor_fds[1], mac_address)
    else:
      # cursor controller process
      plotter_fds[0].close()
      plotter_fds[1].close()
      cursor_fds[1].close()
      cursor_proc(cursor_fds[0], args.linear)
  else:
    # acceleration data plotter process
    plotter_fds[1].close()
    plotter_proc(plotter_fds[0], args.linear)


if __name__ == '__main__':
    main()
