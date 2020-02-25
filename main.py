from datetime import datetime
import matplotlib.pyplot as plt
import pyshark

dataDict = {}
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
counter = 0

print('\n----------------------------------')

cap = pyshark.FileCapture('data/mycapture.pcapng',keep_packets=False)

# wlan layer: wlan
# sniff time: sniff_time

# for x in range(400):
# for x in cap:
    # print(cap[x].sniff_time)
    # print('packet number ' + str(x))

def add_data_to_dict(packet):
        # wlan = cap[x].wlan
        wlan = packet.wlan

        key = wlan.ra
        if key not in dataDict:
            dataDict[key] = 1
        else:
            dataDict[key] = dataDict[key] + 1
        counter += 1

        if counter % 100 == 0:
            print('#',end='')

#     if x % 100 == 0:
#         print("#",end='')
# print('\ndone!')
# receiver address : ra
# destination address: da
# transmitter address: ta
# source address: sa
# vendor lookup api https://macvendors.com/

cap.apply_on_packets(add_data_to_dict)


print(dataDict)
plt.bar(dataDict.keys(),dataDict.values())
plt.xticks(rotation=45,ha="right")
plt.tight_layout()
plt.savefig('figures/' + now,format='eps')
# plt.show()
print('-------------------------\n\n')

