import errno, sys, os
from ble_server import server_proc
from accel_plotter import plotter_proc
from cursor_controller import cursor_proc


mac_addresses = {
  'vincent': '00:3B:40:0B:00:0E',
  'jingbin': '00:09:50:04:00:32',
  'justin': '00:26:50:04:00:30'
}

r, w = os.pipe()
r = os.fdopen(r,'r')
w = os.fdopen(w,'w')


def choose_device():
  if len(sys.argv) != 2 or sys.argv[1] not in mac_addresses:
    sys.stderr.write('usage: python3 {0} user\n  user: vincent, jingbin, or justin\n'.format(sys.argv[0]))
    sys.exit(errno.errorcode[errno.EINVAL])
  return mac_addresses[sys.argv[1]]


def main():
  mac_address = choose_device()
  pid1 = os.fork()
  if pid1:
    pid2 = os.fork()
    if pid2:
      # BLE server process
      r.close()
      server_proc(w, mac_address)
    else:
      # cursor controller process
      w.close()
      cursor_proc(r)
  else:
    # acceleration data plotter process
    w.close()
    plotter_proc(r)


if __name__ == '__main__':
    main()
