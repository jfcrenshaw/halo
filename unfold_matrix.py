#!/usr/bin/env python

import numpy as np

from modules.truth import truth
from modules.efficiency_matrix import effmatrix


inputfile = "input.txt"
truth = truth(inputfile) # dictionary of inputs

for config in truth:
    
    M = effmatrix(config[:5])
    invM = M.I # inverse matrix

    for pair in truth[config]:

        data_location = './data/'
        obs_name = config+'_'+str(pair[0])+'v'+str(pair[1])+'_observed.npy'
        obs_file = data_location + obs_name

        obs_1n, obs_2n = np.load(obs_file)

        unfolded_1n = []
        unfolded_2n = []

        for i in range(len(obs_1n)):
            unf_1n = obs_1n[i]*invM.item(0,0) + obs_2n[i]*invM.item(0,1)
            unf_2n = obs_1n[i]*invM.item(1,0) + obs_2n[i]*invM.item(1,1)

            unfolded_1n.append(unf_1n)
            unfolded_2n.append(unf_2n)

        unfolded_location = './unfolded_data/'
        unfolded_name = config+'_'+str(pair[0])+'v'+str(pair[1])+ \
                                                        '_unfolded_matrix.npy'
        np.save(unfolded_location+unfolded_name,[unfolded_1n,unfolded_2n])




