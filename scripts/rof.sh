SCREEN_NAME_BRIDGE='bridge'
SCREEN_NAME_LIGHTS_HEART='lights-heart'
StartLights()
{
  rm ../lights/*.pyc
  screen -S $SCREEN_NAME_LIGHTS_HEART -d -m python ../lights/lightsWithHeart.py
}
StopLights()
{
  screen -S $SCREEN_NAME_LIGHTS_HEART -p -0 -X quit
}
StartBridge()
{
  # start bridge
  screen -S $SCREEN_NAME_BRIDGE -d -m python ../udp-tcp-bridge/bridgeAll.py
}

StopBridge()
{
  screen -S $SCREEN_NAME_BRIDGE -p 0 -X quit
}

Lights()
{
  case "$1" in
    'start' )
       StartLights
    ;;
    'stop' )
       StopLights
     ;;
     * )
     echo 'Lights - incorrect option'
     echo 'to start $ rof.sh lights start' 
     echo 'to stop  $ rof.sh lights stop' 
     ;;
  esac
}

Bridge()
{
  case "$1" in
    'start' )
       StartBridge
    ;;
    'stop' )
       StopBridge
     ;;
     * )
     echo 'Bridge - incorrect option'
     echo 'to start $ rof.sh bridge start' 
     echo 'to stop  $ rof.sh bridge stop' 
     ;;
  esac
}

Usage()
{
echo '----------------------------------------------'
echo '----------------------------------------------'
echo '---------ROOM OF THE FUTURE-------------------'
echo '---------Questions: dan@danlofaro.com---------'
echo '----------------------------------------------'
echo '----------------------------------------------'
echo ' '
echo 'USAGE:'
echo 'Options'
echo '    bridge               -  udp to tcp bridge' 
echo '                            for server'
echo '          start          -  starts option'
echo '          stop           -  stops opton'
echo '    lights               -  lights with heart' 
echo '                            beat server'
echo '          start          -  starts option'
echo '          stop           -  stops opton'
echo '----------------------------------------------'
echo '----------------------------------------------'


}

case "$1" in
# bridge info
	'bridge' )
		Bridge $2
        ;;
        'lights' )
                Lights $2
        ;;
        * )
		Usage
	;;
esac
exit 0
