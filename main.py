import matplotlib.pyplot
import pyshark
import sys
import os

mydir = os.path.dirname(__file__)

print('\n----------------------------------')
print('I live in: ' + mydir)


cap = pyshark.FileCapture(mydir + '/data/mycapture.pcapng')
# wlan layer: wlan
# sniff time: sniff_time
currentCap = cap[0]

print(cap[0].sniff_time)
wlan = cap[0].wlan

# receiver address : ra
# destination address: da
# transmitter address: ta
# source address: sa
# vendor lookup api https://macvendors.com/

print('destination address = ' + wlan.da)
print('source address = ' + wlan.sa)
