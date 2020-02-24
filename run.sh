#!/bin/bash

IFACE=wlp0s20f3

iter=1
while [ $iter -le 288 ]
do
	fname=$iter.pcapng
	echo $fname
	tshark -i $IFACE -w "dorm/$fname" -a duration:20
	sleep 280
	iter=$(( $iter + 1 ))
done
