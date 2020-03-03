# Plot retry percentage from 'vendor csv' file
import matplotlib.pyplot as plt
import csv
import time

# Target csv file
file_name = 'ewi-29-02-2020 17:32:43-filted-data-vendor'
# data = list(csv.reader(open('figures/'+file_name+'.csv')))
addr = []
retry = []
total = []
with open('figures/'+file_name+'.csv') as f:
    csvReader = csv.reader(f)
    for row in csvReader:
        addr.append(row[0])
        retry.append(int(row[1]))
        total.append(int(row[2]))
data = zip(addr, retry, total)
data_sorted = sorted(data, key=lambda s: s[2], reverse=True)
data_filted = data_sorted[1:21]

percentage = []
for i in range(len(data_filted)):
    percentage.append(data_filted[i][1]*100 // data_filted[i][2])
# plot package counts
# plt.bar([row[0] for row in data_filted], [row[2] for row in data_filted])
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig('figures/' + file_name + '-total', format='eps')
# plt.close()
# plot retry percentage
plt.bar([row[0] for row in data_filted], percentage)
plt.xticks(rotation=45, ha="right")
plt.axhline(y=20, linestyle='--')
plt.ylim(0,100)
plt.tight_layout()
plt.title('Retry rate versus manufacturers - University entrance')
plt.xlabel('Manufacturer')
plt.ylabel('Retry Rate (%)')
plt.savefig('figures/' + file_name + '-retry', format='svg')
plt.close()

print('done!')
print('-------------------------\n\n')
