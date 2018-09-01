#!/usr/bin/env python

import numpy as np
from modules.efficiency_matrix import effmatrix

def prior_distUnknown():

    tru = [[],[]] # array for truth values
    obs = [[],[]] # array for observed values

    for i in range(251):
        for j in range(int(8./11.*i+0.5)):
            tru[0].append(i)
            tru[1].append(j)
    

    M = effmatrix()

    for i in range(len(tru[0])):
        # calculate observations from efficiency matrix
        oneN_obs = tru[0][i]*M.item(0,0)+tru[1][i]*M.item(0,1)
        twoN_obs = tru[0][i]*M.item(1,0)+tru[1][i]*M.item(1,1)
        obs[0].append(oneN_obs)
        obs[1].append(twoN_obs)

    np.save('priors/prior_distUnknown_truth.npy',tru)
    np.save('priors/prior_distUnknown_observed.npy',obs)

