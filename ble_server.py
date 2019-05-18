# Imports for multiprocessing
from multiprocessing.connection import Client
# Imports for bluetooth
import gatt
import struct
import errno, sys


mac_addresses = {
    'vincent': '00:3B:40:0B:00:0E',
    'jingbin': '00:09:50:04:00:32',
    'justin': '00:26:50:04:00:30'
}


def choose_device():
    if len(sys.argv) != 2 or sys.argv[1] not in mac_addresses:
        sys.stderr.write('usage: python3 {0} user\n  user: vincent, jingbin, or justin\n'.format(sys.argv[0]))
        sys.exit(errno.EINVAL)
    return mac_addresses[sys.argv[1]]


# Setting up bluetooth
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


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
        self.previous_val = 0

    def characteristic_value_updated(self, characteristic, value):
        global cli
        #print("Received alert from Hexiwear {}: {}".format(self.mac_address,val))
        val = struct.unpack('>h',value[0:2])
        val = val[0]
        #print(val)
        dev = 0
        if self.mac_address == DEVICE1:
            dev = 1
        elif self.mac_address == DEVICE2:
            dev = 2
        cli.send("{},{}".format(dev,val))
        self.previous_val = val


def main():
    mac_address = choose_device()
    manager = gatt.DeviceManager(adapter_name='hci0')
    hexiwear = HexiDevice(mac_address=mac_address, manager=manager)
    hexiwear.connect()

    # Multiprocessing client
    # cli = Client(('192.168.43.96', 5005))
    #cli = Client(('localhost',5005))
    manager.run()


if __name__ == '__main__':
    main()
