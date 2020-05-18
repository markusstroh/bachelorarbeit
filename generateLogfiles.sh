#!/bin/bash

# This script generates logfiles that are going to be analysed.

sessionCnt=0
routineCnt=0
daysCnt=0

widget1=$(( (RANDOM % 14) + 1 ))
widget2=$(( (RANDOM % 14) + 1 ))
widget3=$(( (RANDOM % 14) + 1 ))

# Make sure that the three Widgets are different
while [ $widget1 -eq $widget2 ]
do
    widget2=$(( (RANDOM % 14) + 1 ))
done


while (( widget1 == widget3 || widget2 == widget3 ))
do
    widget3=$(( (RANDOM % 14) + 1 ))
done
###

# Generate logfiles for 90 Days
while [ $daysCnt -le  90 ]
do
	sessionsPerDayCnt=1
	maxSessions=0
	maxSessions=$(( (RANDOM % 20) + 1 ))


	while [ $sessionsPerDayCnt -le $maxSessions ]
	do
		if [ $(($sessionsPerDayCnt % 3)) -eq 0 ] # every third session should contain the specified widgets
		then
			python3.7 python/logEntryGenerator.py -d $daysCnt -f=$widget1,$widget2,$widget3
			sessionCnt=$(($sessionCnt + 1))
			routineCnt=$(($routineCnt + 1))
		else
			python3.7 python/logEntryGenerator.py -d $daysCnt
			sessionCnt=$(($sessionCnt +1))
		fi
		sessionsPerDayCnt=$(($sessionsPerDayCnt +1))
	done
	daysCnt=$(($daysCnt +1))
done

echo "$sessionCnt sessions and $routineCnt generated"

echo "$widget1 $widget2 $widget3" > widgets.txt
