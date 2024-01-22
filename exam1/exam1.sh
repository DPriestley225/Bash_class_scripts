#!/bin/bash

#var to save the number of season to pass 450HRs and 1700RBIs
seasons_to_pass=0
#function
stats_check () {
	#$1 HR_total
	#$2 RBI_total
	#$3 the current season
	#added the final and to catch the program from overwriting the first occurence
	if [ $1 -gt 450 ] && [ $2 -gt 1700 ] && [ $seasons_to_pass -lt 1 ]
	then
		seasons_to_pass=$3
	fi
}

#tasks 1
#replace all commas in Teddy Ballgame with spaces 
#and forward to TeddyBallgame.txt
#uses sed to do this
sed 's/,/ /g' TeddyBallgame.csv > TeddyBallgame.txt

#task 2
seasons_total=0
over_one_thirty_seasons=0
HR_total=0
RBI_total=0
#loop here
while read -r line
do

#checks if we are on header line
	if [ $seasons_total -gt 0 ]
	then
		#catching data
		Games=$( echo $line | cut -f 3 -d ' ' )
		HR=$( echo $line | cut -f 4 -d ' ' )
		RBI=$( echo $line | cut -f 5 -d ' ' )
		HR_total=$(( $HR_total + $HR ))
		RBI_total=$(( $RBI_total + $RBI ))

		#check for over 130 games
		if [ $Games -gt 130 ]
			then
	   		(( over_one_thirty_seasons++ ))
			fi

		stats_check $HR_total $RBI_total $seasons_total
	fi
	(( seasons_total++ ))

done < TeddyBallgame.txt

echo "it took Teddy Ballgame $seasons_to_pass seasons to surpase 450 HR and 1700 RBI"
echo "In that time, he player over 130 games $over_one_thirty_seasons times and had $HR_total HR and $RBI_total RBI"

