from datetime import datetime
import matplotlib.pyplot as plt
import pyshark
import os
from mac_vendor_lookup import MacLookup

# check if data and figures folder exist, if not create them
if not os.path.exists('data'):
    os.makedirs('data')
    print('data folder created')
if not os.path.exists('figures'):
    os.makedirs('figures')
    print('figures folder created')


dataDict = {}
# dataDict = [
#   {MAC : {ra_amount: ra_amount, sa_amount: sa_amount, sniff_times: [sniff_times]}}
# ]
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
counter = 0

mac = MacLookup()
mac.load_vendors()

print('\n----------------------------------')

cap = pyshark.FileCapture('data/mycapture.pcapng',keep_packets=False)

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

    if counter % 100 == 0:
        print('#',end='')
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
            vendor = key

        if vendor not in vendorDict:
            vendorDict[vendor] = amount
        else:
            vendorDict[vendor] += amount
        print('#',end='')
    print('')
    return vendorDict

# receiver address : ra
# destination address: da
# transmitter address: ta
# source address: sa
# vendor lookup api https://macvendors.com/

# cap.apply_on_packets(add_data_to_dict,packet_count=500)
cap.apply_on_packets(add_data_to_dict)
print('') # newline to end the progress updates

vendors = get_vendors(dataDict)

print(sum(dataDict.values()) == sum(vendors.values()))

print(dataDict)
print(vendors)
plt.bar(vendors.keys(),vendors.values())
plt.xticks(rotation=45,ha="right")
plt.tight_layout()
plt.savefig('figures/' + now,format='eps')
print('-------------------------\n\n')

