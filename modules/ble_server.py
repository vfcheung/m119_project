import gatt
import struct


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
        #button_input= [struct.unpack('<h', value[2*i:2*i+2])[0] for i in range(4)]
        button_input=struct.unpack('<h', value[6:8])[0]
        to_plotter.write(str(accel_vals) + '\n') #basically put that into a list and print that shit as a list and we good
        to_plotter.flush()
        accel_vals.append(button_input)
        to_cursor.write(str(accel_vals) + '\n')
        to_cursor.flush()


def server_proc(pipe_to_plotter, pipe_to_cursor, mac_address):
    global to_plotter
    global to_cursor

    to_plotter = pipe_to_plotter
    to_cursor = pipe_to_cursor

    print("server process started")
    
    manager = gatt.DeviceManager(adapter_name='hci0')
    hexiwear = HexiDevice(mac_address=mac_address, manager=manager)
    hexiwear.connect()
    manager.run()
