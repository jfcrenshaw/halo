#!/usr/bin/env python

# Note that this script requires ROOT (it runs a ROOT script below).
# It needs to be run on the neutrino computers (or any computer with ROOT)

import os
from convert_files import npy_to_txt, txt_to_npy

config = 2 # 1=HALO, 2=HALO-1kT
dist = [10] # supernova distance in kpc
eff = [0.3,0.35,0.4,0.45,0.50,0.55,0.6,0.65] # 1n detection efficiency

for d in dist:
    for e in eff:

        # observed data
        obsdata = './data/halo'+str(config)+'_'+str(d)+'kpc_observed_E'+str(int(e*100))+'.npy'

        # save a txt version for root to use
        npy_to_txt(obsdata)


	    # ----------------------------------------------------------------------
		# ----------------------------------------------------------------------
		# UNFOLD WITH THE DISTANCE KNOWN PRIORS
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------

        # prior names
        truprior = './priors/prior_halo'+str(config)+'_'+str(d)+'kpc_truth.npy'
        obsprior = './priors/prior_halo'+str(config)+'_'+str(d)+'kpc_observed_E'+\
                    str(int(100*e))+'.npy' 

		# save text versions
        npy_to_txt(truprior)
        npy_to_txt(obsprior)
        npy_to_txt(obsdata)

        scale = (5.0/d)**2
        if config == 2:
            scale /= 0.079

        oneN = 72*scale
        twoN = 48*scale

        # Unfold
        os.system("root -l -q 'unfold_bayesian_root.C({0},{1},{2},{3},{4}\
                    )'".format(config,d,int(e*100),oneN,twoN))

		# save the unfolded text file as npy file
        unfolded  = './unfolded_data/halo'+str(config)+'_'+str(d)+'kpc_unfolded_E'+\
                    str(int(100*e))+'.txt'
        txt_to_npy(unfolded)
        
        # remove text files
        os.system('rm data/*txt')
        os.system('rm priors/*txt')
        os.system('rm unfolded_data/*txt')
		
	
