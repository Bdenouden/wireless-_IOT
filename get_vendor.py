# Get vendor for 'mac address csv' file 
# and write to 'vendor csv' file
import matplotlib.pyplot as plt
import numpy as np
from mac_vendor_lookup import MacLookup
import csv
import requests
import time

# Target csv file
file_name = "ewi-29-02-2020 17:32:43-filted-data"

addr = []
retry = []
total = []
with open('figures/'+file_name+'.csv') as f:
    csvReader = csv.reader(f)
    for row in csvReader:
        addr.append(row[0])
        retry.append(int(row[1]))
        total.append(int(row[2]))

# Vendor lookup
print(' Looking up vendors...')
mlu = MacLookup()
mlu.load_vendors()
url = 'http://api.macvendors.com/'
for i in range(len(addr)):
    # lookup table
    # try:
    #     vendor = mlu.lookup(addr[i])
    # except:
    #     if addr[i]=="ff:ff:ff:ff:ff:ff":
    #         vendor = 'Broadcast'
    #     else:
    #         vendor = 'Other'

    # api
    r = requests.get(url + addr[i])
    time.sleep(1)
    if r.ok:
        vendor = r.text
    else:
        if addr[i] == 'ff:ff:ff:ff:ff:ff':
            vendor = 'Broadcast'
        else:
            vendor = "Other"
    print('.',end='')
    addr[i] = vendor
print('Done')

# Merge duplicates
addr_set = []
retry_set = []
total_set = []
for i in range(len(addr)):
    if addr[i] in addr_set:
        index = addr_set.index(addr[i])
        retry_set[index] += int(retry[i])
        total_set[index] += int(total[i])
    else:
        addr_set.append(addr[i])
        retry_set.append(retry[i])
        total_set.append(total[i])
    

# Export vendors to csv
print(' Exporting csv and plot files...', end='')
with open('figures/'+file_name+'-vendor.csv', 'w') as f:
    w = csv.writer(f)
    for i in range(len(addr_set)):
        row = [addr_set[i],retry_set[i],total_set[i]]
        w.writerow(row)

# Calculate percentage
percentage = []
for i in range(len(addr_set)):
    percentage.append(int(retry_set[i])*100 // int(total_set[i]))

# # plot package counts
# plt.bar(addr_set, total_set)
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig('figures/' + file_name + '-total', format='eps')
# plt.close()
# # plot retry percentage
# plt.bar(addr_set, percentage)
# plt.xticks(rotation=45, ha="right")
# plt.ylim(0,100)
# plt.tight_layout()
# plt.savefig('figures/' + file_name + '-retry', format='eps')
# plt.close()

print('done!')
print('-------------------------\n\n')
