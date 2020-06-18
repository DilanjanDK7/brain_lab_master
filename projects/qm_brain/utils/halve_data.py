import numpy as np

from projects.qm_brain.utils.utils import *

main_path = '/home/user/Desktop/QMBrain/new_movie/'
num_sub = 13

for sub in range(num_sub):
    data_path = main_path + str(sub+1) + '/data.csv'
    data_og = load_matrix(data_path)

    data_new = []

    assert len(data_og.shape) == 2

    if data_og.shape[0]>data_og.shape[1]:
        [data_new.append(data_og[i,:]) for i in range(data_og.shape[0]) if i %2 != 0]
    else:
        [data_new.append(data_og[:,i]) for i in range(data_og.shape[1]) if i % 2 != 0]

    save_file(np.array(data_new), main_path+str(sub+1),'/data_short')
