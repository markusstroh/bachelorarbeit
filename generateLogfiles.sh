#!/bin/bash

# hier muss noch rein, dass man start und ende über das terminal übergibt
sessionCnt=0
i=0 # Anzahl tage
while [ $i -le  31 ]
do
	j=1  # Anzahl der Sessions an einem Tag
	while [ $j -le 11 ]
	do
		if [ $(($j % 3)) -eq 0 ]
		then
			python3.7 python/logEntryGenerator.py -d $i -f
			sessionCnt=$(($sessionCnt +1))
		else
			python3.7 python/logEntryGenerator.py -d $i
			sessionCnt=$(($sessionCnt +1))
		fi
		j=$(($j +1))
	done
	i=$(($i +1))
done

echo "$sessionCnt sessions generated"


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
