import socket
import sys
from thread import *
import time
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port
PORT_HEART = 8890 # heart rate port
PORT_LIGHTS = 8891
PORT_HOME = 8892
PORT_THERMOSTAT = 8893
PORT_SMOKE = 8894
PORT_CAMERA = 8895
PORT_ROBOT = 8896

ports = [PORT, 
         PORT_HEART, 
         PORT_LIGHTS,
         PORT_THERMOSTAT,
         PORT_SMOKE,
         PORT_CAMERA,
         PORT_ROBOT]

robot_message = "none"

joy_left_x = 0.0
joy_left_y = 0.0
joy_right_x = 0.0
joy_right_y = 0.0
message_left = 'left'
message_right = 'right'
message_joy = 'joy'

heart_rate = 0.0
message_heart = 'heart'
message_rate = 'rate'

message_req = 'req'
message_rep = 'rep'

def connectTCP(soc, the_port):
  print 'Socket created'
  #Bind socket to local host and port
  try:
    soc.bind((HOST, the_port))
  except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
  print 'Socket bind complete'
 
  #Start listening on socket
  soc.listen(10)
  print 'Socket now listening'
  return soc


print "1" 
s            = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "2" 
s_heart      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "3" 
s_lights     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "4" 
s_thermostat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "5" 
s_smoke      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "6" 
s_camera     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "7" 
s_robot      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "8" 

print "11" 
s            = connectTCP(s, PORT)
print "22" 
s_heart      = connectTCP(s_heart, PORT_HEART)
print "33" 
s_lights     = connectTCP(s_lights, PORT_LIGHTS)
print "44" 
s_thermostat = connectTCP(s_thermostat, PORT_THERMOSTAT)
print "55" 
s_smoke      = connectTCP(s_smoke, PORT_SMOKE)
print "66" 
s_camera     = connectTCP(s_camera, PORT_CAMERA)
print "77" 
s_robot      = connectTCP(s_robot, PORT_ROBOT)
print "88" 


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    try:
      start_new_thread(udpClientThread ,(conn,))
    #infinite loop so that function do not terminate and thread do not end.
      print "TCP Read"
      while True:
         
        #Receiving from client
        data = conn.recv(1024)
#        reply = 'ref ' + str(0.123) + " " + str(0.456)
        if not data: 
            break
        print data
        
        ds = data.split(" ")
        if len(ds) > 0:
          if ds[0] == message_req:
            if ds[1] == message_joy:
              if len(ds) >= 3:
                if ds[2] == message_left:
                  sendJoystick(conn, message_left, joy_left_x, joy_left_y)
                if ds[2] == message_right:
                  sendJoystick(conn, message_right, joy_right_x, joy_right_y)
            if ds[1] == message_heart:
              if len(ds) >=3:
                if ds[2] == message_rate:
                  sendHeartRate(conn)
                          
        ##conn.sendall(robot_message)
        #conn.sendall(reply)
    except:
      print 'UDP already running'
     
    #came out of loop
    conn.close()
 
#now keep talking with the client

def sendHeartRate(conn):
  reply = message_rep + ' ' + message_rate + ' ' + str(heart_rate)
  conn.sendall(reply)

def sendJoystick(conn, stick, x, y):
  reply = message_rep + ' ' + message_joy + ' ' + stick + ' ' + str(x) + ' ' + str(y)
  conn.sendall(reply)

def udpClientThread(conn):
 try:
  global robot_message
  global joy_left_x
  global joy_left_y
  global joy_right_x
  global joy_right_y
  global heart_rate
  
  
  
  
  robot_message = "no"
  UDP_IP = "10.18.81.7"
  #UDP_IP = "104.131.47.73"
  UDP_PORT = 2362

  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  print "in udp thread"
  while True:
      data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
      robot_message = data
      ds = data.split(" ")
      if ds[0] == message_heart:
        if ds[1] == message_rate:
          if len(ds) >= 3:
            heart_rate = float(ds[2])
      if ds[0] == message_joy:
          if len(ds) >= 4:
            if ds[1] == message_left:
              joy_left_x = float(ds[2])
              joy_left_y = float(ds[3])
            if ds[1] == message_right:
              joy_right_x = float(ds[2])
              joy_right_y = float(ds[3])              
      print "received message:", data
 except:
  print "Can not connect to UDP, port already open" 


def joyThread():
  print 'enter joy'
  while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
  print 'exit joy'
  s.close()

def heartThread():
  print 'enter heart'
  while 1:
    #wait to accept a connection - blocking call
    conn_heart, addr = s_heart.accept()
    
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn_heart,))
  print 'exit heart'
  s_heart.close()

def listenThread(ss):
  print 'enter heart'
  while 1:
    #wait to accept a connection - blocking call
    conn_heart, addr = ss.accept()

    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn_heart,))
  print 'exit heart'
  ss.close()

print 'start thread - heart'
start_new_thread(heartThread ,())
print 'start thread - joy'
start_new_thread(joyThread ,())
print 'start thread - lights'
start_new_thread(listenThread ,(s_lights,))
print 'start thread - thermostat'
start_new_thread(listenThread ,(s_thermostat,))
print 'start thread - smoke'
start_new_thread(listenThread ,(s_smoke,))
print 'start thread - cmaera'
start_new_thread(listenThread ,(s_camera,))
print 'start thread - robot'
start_new_thread(listenThread ,(s_robot,))




while True:
  time.sleep(1)
