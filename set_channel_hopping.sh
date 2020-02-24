#!/bin/bash

IFACE=wlp0s20f3

bg="1 2 3 4 5 6 7 8 9 10 11"
bg_intl="$bg 12 13 14"
a="36 40 44 48 52 56 60 64 149 153 157 161"
bga="$bg $a"
bga_intl="$bg_intl $a"

ifconfig $IFACE down
iwconfig $IFACE mode monitor
ifconfig $IFACE up

while true ; do
	for CHAN in $bg ; do
		iwconfig $IFACE channel $CHAN
		echo "Switching to channel $CHAN"
		sleep 1s
	done
done


