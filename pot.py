from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
from mac_vendor_lookup import MacLookup
import csv

roundOffSecond = 10

mlu = MacLookup()
mlu.load_vendors()

sources = []
tvs = {}

#
# get a timeplot for each mac address, 5 min interval
# get total macs per 5 min
#
#
#
#

def add_data_to_dict(packet):
    source = packet.source[0:17]
    destination = packet.destination[0:17]
    time = packet.time.split('.')[0]
    time = myround(int(time),roundOffSecond)
    if source and destination:
        global sources
        global tvs
        sources.append(source)
        if time not in tvs:
            tvs[time] = [source]
        else:
            if source not in tvs[time]:
                tvs[time].append(source)


        # print ('Time = ' + time + '\tSource = ' + source + '\t\tDestination = ' + destination)

def myround(x, base=5):
    return base * round(x/base)

def getVendors(mac):
    try:
        rMac = mlu.lookup(mac)
    except:
        if "ff:ff:ff:ff:ff:ff" in mac:
            rMac = 'Broadcast 2 '
        rMac = 'Other'
    
    return rMac

cap = pyshark.FileCapture('data/mycapture.pcapng', keep_packets=False, only_summaries=True)
cap.apply_on_packets(add_data_to_dict, packet_count=0)
# for mac in sources:
#     print(getVendors(mac))

plt.bar(tvs.keys(),[len(arr) for arr in tvs.values()], align='center',width=3*roundOffSecond/4)
plt.tight_layout()
plt.show()