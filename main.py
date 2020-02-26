from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
from mac_vendor_lookup import MacLookup
import csv

# check if data and figures folder exist, if not create them
if not os.path.exists('data'):
    os.makedirs('data')
    print('data folder created')
if not os.path.exists('figures'):
    os.makedirs('figures')
    print('figures folder created')


dataDict = {}
timeDict = {}
macTimeDict = {}
# dataDict = [
#   {MAC : {ra_amount: ra_amount, sa_amount: sa_amount, sniff_times: [sniff_times]}}
# ]
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
counter = 0

mac = MacLookup()
mac.load_vendors()

print('\n----------------------------------')

cap = pyshark.FileCapture('data/mycapture.pcapng', keep_packets=False)

# wlan layer: wlan
# sniff time: sniff_time


def add_data_to_dict(packet):
    global counter
    wlan = packet.wlan

    key = wlan.ra
    if key not in dataDict:
        dataDict[key] = 1
    else:
        dataDict[key] = dataDict[key] + 1
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
    print('getting vendors: ')
    for key in keys:
        amount = myDict[key]

        try:
            vendor = mac.lookup(key)
        except:
            if key == 'ff:ff:ff:ff:ff:ff':
                vendor = 'Broadcast'
            else:
                vendor = key

        if vendor not in vendorDict:
            vendorDict[vendor] = amount
        else:
            vendorDict[vendor] += amount
        print('#', end='')
    print('')
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

print('#MAC collected == #vendors: ' +
      str(sum(dataDict.values()) == sum(vendors.values()))
      )

# print('vendors:')
# print(vendors)
plt.bar(vendors.keys(), vendors.values())
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('figures/' + now, format='eps')
plt.close()

print(str(len(list(macTimeDict.keys()))) + ' MAC addresses collected')
# targetMac = list(macTimeDict.keys())[5]
# data1 = macTimeDict[targetMac]
# plt.bar(data1.keys(), data1.values())
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig('figures/' + now + '-mac:' + targetMac, format='eps')


print('Plotting and exporting csv files...', end='')
for targetMac in macTimeDict:
    d = macTimeDict[targetMac]
    path = 'figures/'+now+'-macTime'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path+'/'+targetMac + '.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(d.items())

    plt.bar(d.keys(), d.values())
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path + '/' + targetMac, format='eps')
    plt.close()

print('done!')
print('-------------------------\n\n')
