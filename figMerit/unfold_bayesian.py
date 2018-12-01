#!/usr/bin/env python

# Note that this script requires ROOT (it runs a ROOT script below).
# It needs to be run on the neutrino computers (or any computer with ROOT)

import numpy as np
import os
from convert_files import npy_to_txt, txt_to_npy

config = 2 # 1=HALO, 2=HALO-1kT
dist_uncertainty = [0.1]
dist = [5,10,14] # supernova distance in kpc
eff = np.linspace(0.3,0.8,11) # 1n detection efficiency

for d in dist:
    for du in dist_uncertainty:
        for e in eff:

            # observed data
            obsdata = './data/halo'+str(config)+'_'+str(d)+'kpc_observed_E'+\
                        str(int(e*100))+'.npy'

            # save a txt version for root to use
            npy_to_txt(obsdata)


            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # UNFOLD WITH THE DISTANCE KNOWN PRIORS
            # ------------------------------------------------------------------
            # ------------------------------------------------------------------

            # prior names
            fname = 'prior_halo'+str(config)+'_'+str(int(d))+'kpc'+\
            '_distUncert'+str(int(100*du))
            truprior = './priors/'+fname+'_truth.npy'
            obsprior = './priors/'+fname+'_observed_E'+str(int(100*e))+'.npy' 

            # save text versions
            npy_to_txt(truprior)
            npy_to_txt(obsprior)
            npy_to_txt(obsdata)

            scale = (10.0/d)**2
            if config == 2:
                scale /= 0.079

            oneN = 150*scale
            twoN = 40*scale

            # Unfold
            os.system("root -l -q 'unfold_bayesian_root.C({0},{1},{2},{3},{4},{5}\
                        )'".format(config,d,int(du*100),int(e*100),oneN,twoN))

            # save the unfolded text file as npy file
            unfolded  = './unfolded_data/halo'+str(config)+'_'+str(d)+\
                        'kpc_distUncert'+str(int(100*du))+'_unfolded_E'+\
                        str(int(100*e))+'.txt'
            txt_to_npy(unfolded)
            
            # remove text files
            os.system('rm data/*txt')
            os.system('rm priors/*txt')
            os.system('rm unfolded_data/*txt')
            
        
