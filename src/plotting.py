# plots the score data

from matplotlib import pyplot as plt
import numpy as np
import csv, copy

# process the CSV
data = csv.reader(open("./0201_rollout_results.csv"))
processed = {}
keys = []  # keys of the processed data
header = True  # flag to set the headers
for row in data:  # for each row in the CSV
    if header:  # set the headers
        for item in row:  # for each item
            processed[item] = {}
            processed[item]["iter"] = []  # set the processed data key
            processed[item]["vals"] = []  # set the processed data key
        keys = copy.deepcopy(row)
        header = False  # reset the flag
    else:  # add data to their header
        for i in range(len(row)):
            processed[keys[i]]["iter"].append(row[0])
            processed[keys[i]]["vals"].append(row[i])

print(keys)
# plot the data
fig, (ax1, ax2) = plt.subplots(1, 2)  # create and pull the figure/axis for the plot
print(">", processed["0201_10_20_1_sr"]["iter"], processed["0201_10_20_1_sr"]["vals"])

ax1.plot(processed["0201_10_20_1_sr"]["iter"], processed["0201_10_20_1_sr"]["vals"], label="10_20_1")
#ax1.plot(processed["0201_10_20_2_sr"]["iter"], processed["0201_10_20_2_sr"]["vals"], label="10_20_2")
fig.legend()  # baseline
ax1.set_xlim([0, 800])
ax1.set_xticks(range(0, 800, 100))
#ax1.set_ylim((0, 1))
ax1.set_yticks(np.arange(0, 1, 0.05))
ax1.set_xlabel("Number of Demonstrations Supplied to Baseline DAPG Implementation")
ax1.set_ylabel("Success Ratio of 500-Iteration Policy Rollout")
plt.show()
