#!/usr/bin/bash
rm /home/kostya/home_termometer/temperature.log
/usr/bin/cat /dev/ttyUSB0 > /home/kostya/home_termometer/temperature.log &
sleep 5
/usr/bin/killall /usr/bin/cat

