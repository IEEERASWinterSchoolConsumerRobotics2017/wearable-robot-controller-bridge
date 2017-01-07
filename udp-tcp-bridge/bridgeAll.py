import socket
import sys
from thread import *
import time
 
HOST = '10.18.81.7'   # Symbolic name meaning all available interfaces
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

light_bright = 0.0
light_sat = 0.0
light_hue = 0.0

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
        if len(ds) >= 2:
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
            if ds[1] == 'guest':
              if len(ds) >=3:
                if ds[2] == 'enter':
                  sendGuestEnter(conn)
                if ds[2] == 'intruder':
                  sendGuestIntruder(conn)
            if ds[1] == 'light':
              if len(ds) >=3:
                if ds[2] == 'bright':
                  sendLightBright(conn)
                if ds[2] == 'color':
                  sendLightColor(conn)
            if ds[1] == 'music':
              if len(ds) >=3:
                if ds[2] == 'genre':
                  sendMusicGenre(conn)
            if ds[1] == 'video':
              if len(ds) >=3:
                if ds[2] == 'genre':
                  sendVideoGenre(conn)
            if ds[1] == 'voice':
              if len(ds) >=3:
                if ds[2] == 'genre':
                  sendVoiceGenre(conn)
            if ds[1] == 'thermostat':
              if len(ds) >=3:
                if ds[2] == 'all':
                  sendThermostatAll(conn)
            if ds[1] == 'smoke':
              if len(ds) >=3:
                sendSmoke(conn)
            #if ds[1] == 'camera':
            if ds[1] == 'item':
              if len(ds) >=3:
                if ds[2] == 'des':
                  sendItem(conn)
          if ds[0] == 'set':
           if len(ds) >=3:
            if ds[1] == 'music':
              if len(ds) >=4:
                if ds[2] == 'genre':
                  setMusic(conn,ds[3])
            if ds[1] == 'video':
              if len(ds) >=4:
                if ds[2] == 'genre':
                  setVideo(conn,ds[3])
            if ds[1] == 'voice':
              if len(ds) >=4:
                if ds[2] == 'command':
                  sendSetVoice(conn, ds[3])
            if ds[1] == 'thermostat':
              if len(ds) >=4:
                if ds[2] == 'actual':
                  setThermostatActual(conn, ds[3])
                if ds[2] == 'des':
                  setThermostatDes(conn, ds[3])
            if ds[1] == 'smoke':
              setSmoke(conn,ds[2])
            if ds[1] == 'camera':
              if len(ds) >=5:
                if ds[2] == 'state':
                  setCameraState(conn, ds[3], ds[4])
                if ds[2] == 'image':
                  setCameraImage(conn, ds[3])
            if ds[1] == 'item':
              if len(ds) >=4:
                if ds[2] == 'des':
                  setItemDes(conn, ds[3])
            if ds[1] == 'guest':
              if len(ds) >=4:
                if ds[2] == 'enter':
                  setGuestEnter(conn, ds[3])
            if ds[1] == 'guest':
              if len(ds) >=4:
                if ds[2] == 'intruder':
                  setGuestIntruder(conn, ds[3])
                          
        ##conn.sendall(robot_message)
        #conn.sendall(reply)
    except:
      print 'UDP already running'
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
def sendMusicGenre(conn):
  reply = message_rep + ' ' + 'music' + ' ' + 'genre' + ' ' + music_genre
  conn.sendall(reply)
def sendVideoGenre(conn):
  reply = message_rep + ' ' + 'video' + ' ' + 'genre' + ' ' + video_genre
  conn.sendall(reply)

def sendVoiceGenre(conn):
  reply = message_rep + ' ' + 'voice' + ' ' + 'command' + ' ' + item_cmd
  conn.sendall(reply)


def sendThermostatAll(conn):
  reply = message_rep + ' ' + 'thermostat' + ' ' + 'des' + ' ' + str(thermostat_des) + ' ' + str(thermostat_act)
  conn.sendall(reply)

def sendSmoke(conn):
  reply = message_rep + ' ' + 'smoke' + ' ' + str(smoke_onoff)
  conn.sendall(reply)

def sendItem(conn):
  reply = message_rep + ' ' + 'item' + ' ' + 'des' + ' ' + item_des
  conn.sendall(reply)

music_genre = 'rock'
def setMusic(conn,val):
  global music_genre
  music_genre = val
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

video_genre = 'aciton'
def setVideo(conn, val):
  global video_genre
  video_genre = val
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

voice_cmd = 'cats'
def setVoice(conn,val):
  global voice_cmd
  voice_cmd = val
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

thermostat_act = 0.0
def setThermostatActual(conn,val):
  global thermostat_act
  thermostat_act = float(val)
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

thermostat_des = 0.0
def setThermostatDes(conn, val):
  global thermostat_des
  thermostat_des = float(val)
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

smoke_onoff = 0
def setSmoke(conn, onoff):
  global smoke_onoff
  smoke_onoff = int(onoff)
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

img_name = 'none'
img_time = 'none'
def setCameraState(conn, nname, ttime):
  global img_name
  global img_time 
  img_name = nname
  img_time = ttime
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

img_str = 'none'
def sSetCameraImage(conn, img):
  global img_str
  img_str = img
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

item_des = 'cats'
def setItemDes(conn, buff):
  global item_des
  item_des = buff
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

guest_enter = '1978-01-23-23-59-59'
def setGuestEnter(conn, buff):
  global guest_enter 
  guest_enter = buff
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

intruder_enter = '1978-01-23-23-59-59'
def setGuestIntruder(conn, buff):
  global intruder_enter 
  intruder_enter = buff
  reply = message_rep + ' ' + 'ok'
  conn.sendall(reply)

def sendGuestEnter(conn):
  reply = message_rep + ' ' + 'guest' + ' ' + 'enter' + ' ' + guest_enter
  conn.sendall(reply)

def sendGuestIntruder(conn):
  reply = message_rep + ' ' + 'guest' + ' ' + 'intruder' + ' ' + intruder_enter
  conn.sendall(reply)

def sendLightBright(conn):
  reply = message_rep + ' ' + 'light' + ' ' + 'bright' + ' ' + str(light_bright)
  conn.sendall(reply)

def sendLightColor(conn):
  reply = message_rep + ' ' + 'bright' + ' ' + 'color' + ' ' + str(light_hue) + ' ' + str(light_sat)
  conn.sendall(reply)

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
