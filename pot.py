from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
import sys
from mac_vendor_lookup import MacLookup
import csv
import numpy as np

roundOffSecond = 10

mlu = MacLookup()
mlu.load_vendors()

# sources = []
tvs = {} # time versus source

def add_data_to_dict(packet):
    source = packet.source[0:17]
    destination = packet.destination[0:17]
    # time = packet.time.split('.')[0]
    # time = myround(int(time),roundOffSecond)
    global time

    if source and destination:
        # global sources
        global tvs
        # sources.append(source)
        if time not in tvs:
            tvs[time] = [source]
        else:
            if source not in tvs[time]:
                tvs[time].append(source)

        # print ('Time = ' + time + '\tSource = ' + source + '\t\tDestination = ' + destination)


# def myround(x, base=5):
#     return base * round(x/base)


def getVendors(mac):
    try:
        rMac = mlu.lookup(mac)
    except:
        if "ff:ff:ff:ff:ff:ff" in mac:
            rMac = 'Broadcast 2 '
        rMac = 'Other'

    return rMac

number_of_files = 271
for i in range(1,number_of_files+1): 
    # file = 'data/mycapture.pcapng'
    file = 'data/dorm/'+str(i)+'.pcapng'
    try:
        epoch = int(os.path.getmtime(file)+0.5)
        time = datetime.fromtimestamp(epoch).strftime('%H:%M:%S')

        cap = pyshark.FileCapture(file, keep_packets=False, only_summaries=True)
        cap.apply_on_packets(add_data_to_dict, packet_count=0)
    except:
        print('could not open file ' + str(i))
    sys.stdout.write("\r progress: "+str(i)+' / '+ str(number_of_files)+' files done')
    sys.stdout.flush()
print('')
# for mac in sources:
#     print(getVendors(mac))

labels = list(tvs.keys())
for i in range(len(labels)):
    if not i % 6 == 0:
        labels[i] = ''

plt.bar(tvs.keys(), [len(arr) for arr in tvs.values()], align='center')
plt.xticks(range(number_of_files),labels, rotation=45, ha="right")
plt.tight_layout()
plt.show()
