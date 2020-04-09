#!/bin/bash

# hier muss noch rein, dass man start und ende über das terminal übergibt

i=24
while [ $i -le  54 ]
do
	j=1
	while [ $j -le 11 ]
	do
		if [ $(($i % 3)) -eq 0 ]
		then
			python3.7 logEntryGenerator.py -d $i -f
		else
			python3.7 logEntryGenerator.py -d $i
		fi
		j=$(($j +1))
	done
	i=$(($i +1))
done



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
