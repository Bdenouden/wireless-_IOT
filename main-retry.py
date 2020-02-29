from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
from mac_vendor_lookup import MacLookup
import csv
import requests
import time

# check if data and figures folder exist, if not create them
if not os.path.exists('data'):
    os.makedirs('data')
    print('data folder created')
if not os.path.exists('figures'):
    os.makedirs('figures')
    print('figures folder created')


dataDict = {}
timeDict = {}
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
counter = 0

mac = MacLookup()
mac.load_vendors()

print('\n----------------------------------')

cap = pyshark.FileCapture('data/dorm/1.pcapng', keep_packets=False)

# wlan layer: wlan
# sniff time: sniff_time


def add_data_to_dict(packet):
    global counter
    wlan = packet.wlan

    try:
        key = wlan.ra
    except:
        return
    try:
        re = wlan.fc_retry
    except:
        return

    if key not in dataDict:
        dataDict[key] = {}
        dataDict[key]['total'] = 1
        dataDict[key]['retry'] = 0
    else:
        dataDict[key]['total'] += 1

    if re == '1':
        dataDict[key]['retry'] += 1
    
# dataDict = {MAC_address:{
#       total:#total
#       retry:#retry
#   }
# }
#
# macproperties = dataDict[myMac] ( = {total:...., retry:.....})
# macproperties[total] = #total
# percentage = macproperties[retry]/macproperties[total]
# 
    
    counter += 1

    time = packet.sniff_time.strftime("%d-%m-%Y %H:%M:%S")
    if time not in timeDict:
        timeDict[time] = [key]
    else:
        if key not in timeDict[time]:  # remove duplicate entries
            timeDict[time].append(key)

    if counter % 100 == 0:
        print('#', end='')
    if counter % 5000 == 0:
        print('!!')


def get_vendors(myDict):
    vendorDict = {}
    keys = myDict.keys()
    url = 'http://api.macvendors.com/'
    print('getting vendors....',end='')
    for key in keys:
        amount = myDict[key]

        # try:
        #     vendor = mac.lookup(key)
        # except:
        #     if key == 'ff:ff:ff:ff:ff:ff':
        #         vendor = 'Broadcast'
        #     else:
        #         vendor = key

        r = requests.get(url + key)
        time.sleep(1)
        if r.ok:
            vendor = r.text
            print(r.text)
        else:
            if key == 'ff:ff:ff:ff:ff:ff':
                vendor = 'Broadcast'
            else:
                vendor = key

        if vendor not in vendorDict:
            vendorDict[vendor] = {}
            vendorDict[vendor]['total'] = amount['total']
            vendorDict[vendor]['retry'] = amount['retry']
        else:
            vendorDict[vendor]['total'] += amount['total']
            vendorDict[vendor]['retry'] += amount['retry']
    print('done!')
    return vendorDict


def getPresenceOverTime():
    macs = list(dataDict.keys())
    # {mac : {DateTime: True/False}} t/f indicates if mac address was present at that time
    macTimeDict = {}

    for ti in timeDict:  # ti is time string
        # all mac addresses that occured on this timestamp
        macs_in_ti = timeDict[ti]

        for mac in macs_in_ti:
            if mac not in macTimeDict:
                macTimeDict[mac] = {ti: True}
            else:
                # add or create timestamp true
                macTimeDict[mac].update({ti: True})

        macs_not_in_ti = list(set(macs) - set(macs_in_ti))
        for mac in macs_not_in_ti:  # add false for all mac adresses not in timestamp
            if mac not in macTimeDict:
                macTimeDict[mac] = {ti: False}
            else:
                # add or create timestamp true
                macTimeDict[mac].update({ti: False})

        if len(list(set(macs)-set(list(macTimeDict.keys())))) != 0:
            print('somethings wrong.....')
    return macTimeDict
# receiver address : ra
# destination address: da
# transmitter address: ta
# source address: sa
# vendor lookup api https://macvendors.com/


cap.apply_on_packets(add_data_to_dict, packet_count=5000)
# cap.apply_on_packets(add_data_to_dict)
print('')  # newline to end the progress updates

macTimeDict = getPresenceOverTime()
vendors = get_vendors(dataDict)

print('Plotting and exporting csv files...', end='')
fields = ['addr', 'retry', 'total']
with open('figures/'+now+'-vendordata.csv', 'w') as f:
    w = csv.DictWriter(f,fields)
    for key,val in vendors.items():
        row = {'addr': key}
        row.update(val)
        w.writerow(row)
    #w.writerows(vendors.items())


filter_vendor={}
for vendor in vendors:
    if vendors[vendor]['total'] >= 10:
        filter_vendor[vendor] =  vendors[vendor]['total']


# print('#MAC collected == #vendors: ' +
#       str(sum(dataDict.values()) == sum(filter_vendors.values()))
#       )

# print('vendors:')
# print(vendors)
retryDict = {}
for key in filter_vendor:
    retryDict[key] =1
    retryDict[key] = 100 * vendors[key]['retry'] / vendors[key]['total']

plt.bar(filter_vendor.keys(), filter_vendor.values())
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('figures/' + now + '-total', format='eps')
plt.close()
plt.bar(retryDict.keys(), retryDict.values())
plt.xticks(rotation=45, ha="right")
plt.ylim(0,100)
plt.tight_layout()
plt.savefig('figures/' + now + '-retry', format='eps')
plt.close()

print(str(len(list(macTimeDict.keys()))) + ' MAC addresses collected')

# print('Plotting and exporting csv files...', end='')
# for targetMac in macTimeDict:
#     d = macTimeDict[targetMac]
#     path = 'figures/'+now+'-macTime'

#     if not os.path.exists(path):
#         os.makedirs(path)

#     with open(path+'/'+targetMac + '.csv', 'w') as f:
#         w = csv.writer(f)
#         w.writerows(d.items())

#     plt.bar(d.keys(), d.values())
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()
#     plt.savefig(path + '/' + targetMac, format='eps')
#     plt.close()

# print('done!')
print('-------------------------\n\n')
