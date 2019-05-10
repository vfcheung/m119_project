from multiprocessing.connection import Client
import time

c = Client(('localhost', 5000))

count = 0

while True:
    c.send("count is: {}".format(count))
    count = count + 1
    if count > 20:
        count = 0
    print("Got back:", c.recv())
    time.sleep(0.1)
