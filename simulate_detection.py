#!/usr/bin/env python

import numpy as np

from modules.truth import truth
from modules.efficiency_matrix import effmatrix


inputfile = "input.txt"
truth = truth(inputfile)


ntrials = 10000 # how many trials to run


for config in truth:

    M = effmatrix(config[:5])
    
    for pair in truth[config]:
        tru = [[],[]] # array for truth values
        obs = [[],[]] # array for observed values
        
        for i in range(ntrials):
            
            # number of truth events
            truth_1n = np.random.poisson(pair[0])
            truth_2n = np.random.poisson(pair[1])
            
            # calculate observed numbers
            observed = [0.0,0.0]
            for j in range(truth_1n):
                rand = np.random.uniform(0,1)
                if rand <= M.item(0,0):
                    observed[0] += 1.0
                elif rand > M.item(0,0) and rand <= M.item(0,0) + M.item(1,0):
                    observed[1] += 1.0
            for j in range(truth_2n):
                rand = np.random.uniform(0,1)
                if rand <= M.item(0,1):
                    observed[0] += 1.0
                elif rand > M.item(0,1) and rand <= M.item(0,1) + M.item(1,1):
                    observed[1] += 1.0
        
            # add the truth and observed to the master list
            tru[0].append(truth_1n)
            tru[1].append(truth_2n)
            obs[0].append(observed[0])
            obs[1].append(observed[1])
            
        # Save the file for this config/pair
        data_location = './data/'
        output_truth = config+'_'+str(pair[0])+'v'+str(pair[1])+'_truth.npy'
        output_obs = config+'_'+str(pair[0])+'v'+str(pair[1])+'_observed.npy'
        np.save(data_location+output_truth,tru)
        np.save(data_location+output_obs,obs)