#!/bin/bash

# hier muss noch rein, dass man start und ende über das terminal übergibt
sessionCnt=0
routineCnt=0
i=0 # Anzahl tage

widget1=$(( (RANDOM % 14) + 1 ))
widget2=$(( (RANDOM % 14) + 1 ))
widget3=$(( (RANDOM % 14) + 1 ))

while [ $widget1 -eq $widget2 ]
do
    widget2=$(( (RANDOM % 14) + 1 ))
done


while (( widget1 == widget3 || widget2 == widget3 ))
do
    widget3=$(( (RANDOM % 14) + 1 ))
done

while [ $i -le  31 ]
do
	j=1  # Anzahl der Sessions an einem Tag
	k=0

	while [ $k -lt 3 ]
	do
	  k=$(( (RANDOM % 20) + 1 ))
	done

	while [ $j -le $k ]
	do
		if [ $(($j % 3)) -eq 0 ]
		then
			python3.7 python/logEntryGenerator.py -d $i -f=$widget1,$widget2,$widget3
			sessionCnt=$(($sessionCnt + 1))
			routineCnt=$(($routineCnt + 1))
		else
			python3.7 python/logEntryGenerator.py -d $i
			sessionCnt=$(($sessionCnt +1))
		fi
		j=$(($j +1))
	done
	i=$(($i +1))
done

echo "$sessionCnt sessions and $routineCnt generated"

echo "$widget1 $widget2 $widget3" > widgets.txt


#i=1
#while [ $i -le 5 ]
#do
#	if [ $(($i % 2)) -eq 0 ]
#	then
#		echo "jawoll alder $i"
#	fi
#	echo "Welcome $i times"
#	i=$(($i +1))
#done
