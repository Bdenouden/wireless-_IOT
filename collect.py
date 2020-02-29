# loop all data files and write to 'mac address csv'
from datetime import datetime
import pyshark
import sys
import csv

def add_data_to_dict(packet):
    key = packet.destination[0:17]
    info = packet.info
    try:
        retry = info.split("Flags=")[1][4]
    except:
        return
    
    if key not in dataDict:
        dataDict[key] = {}
        dataDict[key]['total'] = 1
        dataDict[key]['retry'] = 0
    else:
        dataDict[key]['total'] += 1

    if (retry == 'R'):
        dataDict[key]['retry'] += 1

def filtAddress(addrDict, bound=5):
    filtedDict = {}
    for addr in addrDict.keys():
        if addrDict[addr]['total'] >= bound:
            filtedDict[addr] =  addrDict[addr]
    return filtedDict


# define parameters
data_set = 'dorm' # dataset ditectory
number_of_files = 271
bound = 20 # filter lower bound

dataDict = {}
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Read all pcapng files
print('\n-----Read-File--------------' + data_set)
for i in range(1,number_of_files+1): 
    file = 'data/' + data_set + '/'+str(i)+'.pcapng'
    try:
        cap = pyshark.FileCapture(file, keep_packets=False, only_summaries=True)
        cap.apply_on_packets(add_data_to_dict, packet_count=0)
    except:
        print('could not open file ' + str(i))
    sys.stdout.write("\r progress: "+str(i)+' / '+ str(number_of_files)+' files done')
    sys.stdout.flush()
print('\n----------------------------')


# Filte out addresses with < bound packages
filtedDict = filtAddress(dataDict, bound)
# Export csv files
print(' Exporting csv files...')
print('   ' + data_set + '-' + now + '-data.csv')
fields = ['addr', 'retry', 'total']
with open('figures/'+data_set+ '-' +now+'-data.csv', 'w') as f:
    w = csv.DictWriter(f,fields)
    for key,val in dataDict.items():
        row = {'addr': key}
        row.update(val)
        w.writerow(row)
print('   ' + data_set + '-' + now + '-filted-data.csv')
with open('figures/'+data_set+ '-' +now+'-filted-data.csv', 'w') as f:
    w = csv.DictWriter(f,fields)
    for key,val in filtedDict.items():
        row = {'addr': key}
        row.update(val)
        w.writerow(row)
print(' ...done!\n')

