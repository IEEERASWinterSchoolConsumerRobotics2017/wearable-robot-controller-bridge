#!/usr/bin/env python3

import time
import numpy as np

import socket

UDP_IP = "192.168.1.188"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

#sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))






while True:
    host = "10.18.81.7"
    #host = "104.131.47.73"
    port = 8890
     
    mySocket = socket.socket()
    mySocket.connect((host,port))
    
    while True:
      message = "req heart rate"
      mySocket.send(message.encode())
      data = mySocket.recv(1024).decode()
      #data = mySocket.recv(1024)
      print(data)
      time.sleep(0.25)
    



