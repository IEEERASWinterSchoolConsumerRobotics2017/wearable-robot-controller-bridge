from phue import Bridge
import time
b = Bridge('192.168.0.105')
b.connect()
b.get_api()

bed_left = 3
bed_right = 4
table = 5

the_max = 255
the_min = 0
T = 2.0

while True:
  b.set_light(bed_left,  'bri', the_max)
  b.set_light(bed_right, 'bri', the_max)
  b.set_light(table,     'bri', the_max)
  time.sleep(T/2.0)
  
  b.set_light(bed_left,  'bri', the_min)
  b.set_light(bed_right, 'bri', the_min)
  b.set_light(table,     'bri', the_min)
  time.sleep(T/2.0)
