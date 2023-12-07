#!/usr/bin/bash

run_not_ok=1
run_not_ok_deamon=4

sleep 2

count=$(ps -aux | grep -w "cctv_monitoring.sh" | wc -l)
if [ $count -eq $run_not_ok_deamon ]; then
  echo "Deamon has restared" >> /home/kostya/home_termometer/cctv/cctv_monitoring.log
else
  echo "Daemon is working now $count $run_not_ok_deamon" >> /home/kostya/home_termometer/cctv/cctv_monitoring.log
  exit
fi

while true
do
	count=$(ps -aux | grep -w "cctv_processor" | wc -l)
	if [ $count -eq $run_not_ok ]; then
	  echo "Restart before" >> /home/kostya/home_termometer/cctv/cctv_monitoring.log
	  /usr/bin/python3 /home/kostya/home_termometer/cctv/cctv_processor.py &
	  sleep 1
	  echo "Restared" >> /home/kostya/home_termometer/cctv/cctv_monitoring.log
	else
	  sleep 1
	fi
done
