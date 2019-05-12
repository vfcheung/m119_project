import time
import serial

print("Starting program")

ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS
                    )

time.sleep(1)

try:
    while True:
        ser.write('Hello World\r\n'.encode())
    #ser.write('Serial comm using Raspberry'.encode())
    '''
    print('Data echo')
    while True:
        if ser.inWaiting()>0:
            data = ser.read()
            print(data)
    '''
except KeyboardInterrupt:
    print("Exiting")

finally:
    ser.close()
    pass
