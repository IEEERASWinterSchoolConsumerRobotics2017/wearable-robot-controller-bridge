#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Drive Cozmo's wheels, lift and head motors directly

This is an example of how you can also have low-level control of Cozmo's motors
(wheels, lift and head) for fine-grained control and ease of controlling
multiple things at once.
'''

import time
import numpy as np

import cozmo

import socket

UDP_IP = "192.168.1.188"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))






while True:
    host = "10.18.81.7"
    #host = "104.131.47.73"
    port = 8889
     
    mySocket = socket.socket()
    mySocket.connect((host,port))
    
    while True:
      message = "req joy left"
      mySocket.send(message.encode())
      data = mySocket.recv(1024).decode()
      #data = mySocket.recv(1024)
      print(data)
      time.sleep(0.1)
    



