# Plot retry percentage from 'vendor csv' file
import matplotlib.pyplot as plt
import csv
import time

# Target csv file
file_name = 'ewi-29-02-2020 17:32:43-filted-data-vendor'
data = list(csv.reader(open('figures/'+file_name+'.csv')))
percentage = []
for i in range(len(data)):
    percentage.append(int(data[i][1])*100 // int(data[i][2]))

# plot package counts
plt.bar([row[0] for row in data], [int(row[2]) for row in data])
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('figures/' + file_name + '-total', format='eps')
plt.close()
# plot retry percentage
plt.bar([row[0] for row in data], percentage)
plt.xticks(rotation=45, ha="right")
plt.ylim(0,100)
plt.tight_layout()
plt.savefig('figures/' + file_name + '-retry', format='eps')
plt.close()

print('done!')
print('-------------------------\n\n')
