import pickle

path = '/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/'

indices = [10, 14]

# Collecting the failure demo
# failure_file = open(path + '0102/failures/0102_10_1_failures.pickle', 'rb')

# failures = pickle.load(failure_file)

# failures_to_fix = []
# for index in indices:
#     print(failures[index])
#     failures_to_fix.append(failures[index])
# failure_to_fix_file = open(path + '0102/failures/0102_10_1_fix_failures.pickle', 'wb')
# pickle.dump(failures_to_fix, failure_to_fix_file)


# Writing correction to file
corr_fix_file = open(path + '0102/corrections/0102_10_1_fix_corrections.pickle', 'rb')
corr_fix = pickle.load(corr_fix_file)
correction_file = open(path + '0102/corrections/0102_10_1_corrections.pickle', 'rb')
corrections = pickle.load(correction_file)

import copy

for i, index in enumerate(indices):
    corrections[index] = copy.deepcopy(corr_fix[i])
    corrections[index]['actions'] == corr_fix[i]['actions'] # check
correction_file = open(path + '0102/corrections/0102_10_1_corrections.pickle', 'wb')
pickle.dump(corrections, correction_file)
