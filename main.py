import os
import sys

import matplotlib.pyplot as plt
import pyshark

dataDict = {

}

mydir = os.path.dirname(__file__)

print('\n----------------------------------')
# print('I live in: ' + mydir)


cap = pyshark.FileCapture(mydir + '/data/mycapture.pcapng')
# wlan layer: wlan
# sniff time: sniff_time

for x in range(400):
# for x in cap:
    # print(cap[x].sniff_time)
    # print('packet number ' + str(x))
    try:
        wlan = cap[x].wlan
        key = wlan.ra
        if key not in dataDict:
            dataDict[key] = 1
        else:
            dataDict[key] = dataDict[key] + 1
    except: 
        y = 1
        # print('line ' + str(x) + 'could not be printed')
# receiver address : ra
# destination address: da
# transmitter address: ta
# source address: sa
# vendor lookup api https://macvendors.com/

    # print('destination address = ' + wlan.da)
    # print('source address = ' + wlan.sa)
    # print('\n')

print(dataDict)
plt.bar(dataDict.keys(),dataDict.values())
plt.xticks(rotation=45)
plt.show()
print('-------------------------\n\n')

