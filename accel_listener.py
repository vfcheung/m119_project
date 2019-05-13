# Imports for multiprocessing
from multiprocessing.connection import Client
# Imports for bluetooth
import gatt
import struct

# Multiprocessing client
cli = Client(('localhost', 5000))

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
        val = value[0]
        #print("Received alert from Hexiwear {}: {}".format(self.mac_address,val))
        #val = struct.unpack('h',value)
        #val = value[0]
        cli.send("{}".format(val))
        self.previous_val = val


# Connect bluetooth
DEVICE1 = "00:09:50:04:00:32"

manager = gatt.DeviceManager(adapter_name='hci0')

hexiwear1 = HexiDevice(mac_address=DEVICE1, manager=manager)
hexiwear1.connect()

manager.run()


