# Imports for multiprocessing
from multiprocessing.connection import Client
# Imports for bluetooth
import gatt
import struct
import errno, sys, os, select

r, w = os.pipe()
r = os.fdopen(r,'r')
w = os.fdopen(w,'w')

mac_addresses = {
    'vincent': '00:3B:40:0B:00:0E',
    'jingbin': '00:09:50:04:00:32',
    'justin': '00:26:50:04:00:30'
}


def choose_device():
    if len(sys.argv) != 2 or sys.argv[1] not in mac_addresses:
        sys.stderr.write('usage: python3 {0} user\n  user: vincent, jingbin, or justin\n'.format(sys.argv[0]))
        sys.exit(errno.errorcode[errno.EINVAL])
    return mac_addresses[sys.argv[1]]


class HexiDevice(gatt.Device):
    
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        device_alert_service = next(
            s for s in self.services
            if s.uuid == '00002030-0000-1000-8000-00805f9b34fb')

        device_alert_out_characteristic = next(
            c for c in device_alert_service.characteristics
            if c.uuid == '00002032-0000-1000-8000-00805f9b34fb')

        device_alert_out_characteristic.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        accel_vals = [struct.unpack('<h', value[2*i:2*i+2])[0] for i in range(3)]
        w.write(str(accel_vals) + '\n')
        w.flush()


def server_main():
    print("server process")
    mac_address = choose_device()
    manager = gatt.DeviceManager(adapter_name='hci0')
    hexiwear = HexiDevice(mac_address=mac_address, manager=manager)
    hexiwear.connect()
    manager.run()


def plotter_main():
    print("plotter process")
    while True:
        print(r.readline(), end='')


def main():
    processid = os.fork()
    if processid:
        # parent
        r.close()
        server_main()
    else:
        # child
        w.close()
        plotter_main()
    


if __name__ == '__main__':
    main()


