#!/bin/bash
#x=1
#while [ $x -le 2 ]
#do
	rm -r data/
	./filebeat -e -c filebeat.yml -d "publish"
#	pid=$!
#	sleep 20
#	kill $pid
#done
