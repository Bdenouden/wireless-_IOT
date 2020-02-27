from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
from mac_vendor_lookup import MacLookup
import csv

mlu = MacLookup()
mlu.load_vendors()

sources = []
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
    if source and destination:
        global sources
        sources.append(source)
        print ('Time = ' + time + '\tSource = ' + source + '\t\tDestination = ' + destination)


def getVendors(mac):
    try:
        rMac = mlu.lookup(mac)
    except:
        if "ff:ff:ff:ff:ff:ff" in mac:
            rMac = 'Broadcast 2 '
        rMac = 'Other'
    
    return rMac

cap = pyshark.FileCapture('data/mycapture.pcapng', keep_packets=False, only_summaries=True)
cap.apply_on_packets(add_data_to_dict, packet_count=100)
for mac in sources:
    print(getVendors(mac))