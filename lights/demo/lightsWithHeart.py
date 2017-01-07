#!/usr/bin/env python
from phue import Bridge
import numpy as np

import socket
import time
b = Bridge('10.18.81.40')
#b = Bridge('192.168.0.105')
time.sleep(1.0)
b.connect()
time.sleep(1.0)
b.get_api()
time.sleep(1.0)

bed_left = 3
bed_right = 4
table = 5

the_max = 255
the_min = 100
T = 2.0

while True:
  host = "104.131.47.73"
  port = 8890
     
  mySocket = socket.socket()
  mySocket.connect((host,port))
    
  while True:
      message = "req heart rate"
      mySocket.send(message.encode())
      data = mySocket.recv(1024).decode()
      #data = mySocket.recv(1024)
      print(data)
      #time.sleep(0.25)
      
      split_data = data.split(" ")
      
      T = float(split_data[2]) / 60.0 * 2.0
      print T
      
      b.set_light(bed_left,  'bri', the_max)
      b.set_light(bed_right, 'bri', the_max)
      b.set_light(table,     'bri', the_max)
      time.sleep(T/2.0)
  
      b.set_light(bed_left,  'bri', the_min)
      b.set_light(bed_right, 'bri', the_min)
      b.set_light(table,     'bri', the_min)
      time.sleep(T/2.0)
  break
