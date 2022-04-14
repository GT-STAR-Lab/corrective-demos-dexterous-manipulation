import pickle
import numpy as np

path = "/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/0201/corrections/0201_10_corrections.pickle"

demos = pickle.load(open(path, "rb"))

for i in range(len(demos)):
    print(i, demos[i]['actions'].shape, demos[i]['observations'].shape)
    
