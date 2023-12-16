#!/usr/bin/bash

run_not_ok=1
#run_not_ok_deamon=4
run_not_ok_deamon=4

sleep 2


count=$(ps -aux | grep -w "cctv_monitoring.sh $1" | wc -l)
if [ $count -eq $run_not_ok_deamon ]; then
  echo "Deamon has restared"
  echo "Deamon has restared" >> /home/kostya/home_termometer/cctv/cctv_monitoring$1.log
else
  echo "Daemon is working now $count $run_not_ok_deamon"
  echo "Daemon is working now $count $run_not_ok_deamon" >> /home/kostya/home_termometer/cctv/cctv_monitoring$1.log
  exit
fi

while true
do
	count=$(ps -aux | grep -w "cctv_processor.py $1" | wc -l)
	if [ $count -eq $run_not_ok ]; then
	  echo "Restart before" >> /home/kostya/home_termometer/cctv/cctv_monitoring$1.log
	  /usr/bin/python3 /home/kostya/home_termometer/cctv/cctv_processor.py $1 &
	  sleep 1
	  echo "Restared" >> /home/kostya/home_termometer/cctv/cctv_monitoring$1.log
	else
	  sleep 1
	fi
done
