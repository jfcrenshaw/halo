#!/usr/bin/env python

# Note that this script requires ROOT (it runs a ROOT script below).
# It needs to be run on the neutrino computers (or any computer with ROOT)

import os
from modules.truth import truth
from modules.convert_files import npy_to_txt, txt_to_npy

inputfile = "input.txt"
truth = truth(inputfile) # dictionary of inputs

# Bayesian Unfolding
for config in truth:
	for pair in truth[config]:

		config_num = config[4]
		config_dist = config[6:-3]
		oneN = pair[0]
		twoN = pair[1]

		# First we need to convert the numpy arrays for the prior and data
		# to normal text files so that root can use them

		# file names
		truprior = './priors/prior_halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_truth.npy'
		obsprior = './priors/prior_halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_observed.npy' 
		obsdata  = './data/halo'+str(config_num)+'_'+str(config_dist)+'kpc_'+\
					str(oneN)+'v'+str(twoN)+'_observed.npy'

		# save text versions
		npy_to_txt(truprior)
		npy_to_txt(obsprior)
		npy_to_txt(obsdata)

		# Unfold
		os.system("root -l -q 'modules/unfold_bayesian_root.C({0},{1},{2},{3})'".format(config_num,config_dist,oneN,twoN))

		# save text files as npy files
		txt_to_npy(truprior)
		txt_to_npy(obsprior)
		txt_to_npy(obsdata)

		# remove the text files
		os.system('rm unfolded_data/*txt')
		os.system('rm priors/*txt')
