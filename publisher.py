import paho.mqtt.client as mqtt
import gatt
import struct
import argparse, textwrap

DEVICE1 = ""
DEVICE2 = ""

def parse_arguments():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--device_add",dest="mac_add",type=str,default="mac.txt")
    return parser.parse_args()

#define callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def publish_buttons(mac,button):
    topic = "ecem119/2019s/hexiwear/{}".format(mac)
    msg = "event {}".format(button)
    print("Publishing msg: {} to topic {}".format(msg, topic))
    info = client.publish(topic,msg)
    info.wait_for_publish()
    print("Publishing result is {}".format(mqtt.error_string(info.rc)))

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
        val = value[0]
        print("Received alert from Hexiwear {}: {}".format(self.mac_address,val))
        #val = struct.unpack('h',value)
        #val = value[0]
        button = "empty"
        if (val == 0):
            button = "empty"
        elif (val == 1):
    	    button = "up"
        elif (val == 2):
    	    button = "down"
        elif (val == 3):
    	    button = "right"
        elif (val == 4):
    	    button = "left"
        else:
    	    button = "nani"
        if ((button != "empty") and (val != self.previous_val)):
            publish_buttons(self.mac_address,button)
        self.previous_val = val


if __name__ == "__main__":

    args = parse_arguments()
    mac_add_file = args.mac_add

    # Read device addresses
    with open(mac_add_file) as f:
        content = f.readlines()
    devices = [x.strip() for x in content]

    DEVICE1 = devices[0]
    DEVICE2 = devices[1]

    # Set up broker
    broker="broker.hivemq.com"

    client = mqtt.Client("publisher") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) 
    ######Bind function to callback
    client.on_coonnect = on_connect
    #####
    print("connecting to broker ",broker)
    client.connect(broker,1883)

    # Set up bluetooth
    manager = gatt.DeviceManager(adapter_name='hci0')

    hexiwear1 = HexiDevice(mac_address=DEVICE1, manager=manager)
    hexiwear1.connect()

    hexiwear2 = HexiDevice(mac_address=DEVICE2, manager=manager)
    hexiwear2.connect()

    manager.run()



#LINKS:
#http://www.steves-internet-guide.com/python-mqtt-publish-subscribe/
#https://pypi.org/project/paho-mqtt/#connect-reconnect-disconnect
#http://www.steves-internet-guide.com/client-connections-python-mqtt/
#http://www.steves-internet-guide.com/mqtt-works/
#http://www.steves-internet-guide.com/
