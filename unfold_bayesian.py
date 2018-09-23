#!/usr/bin/env python

# Note that this script requires ROOT (it runs a ROOT script below).
# It needs to be run on the neutrino computers (or any computer with ROOT)

from modules.truth import truth
from modules.npy_to_txt import npy_to_txt

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
		trudata  = './data/halo'+str(config_num)+'_'+str(config_dist)+'kpc_'+\
					str(oneN)+'v'+str(twoN)+'_truth.npy'
		obsdata  = './data/halo'+str(config_num)+'_'+str(config_dist)+'kpc_'+\
					str(oneN)+'v'+str(twoN)+'_observed.npy'

		# save text versions
		npy_to_txt(truprior)
		npy_to_txt(obsprior)
		npy_to_txt(trudata)
		npy_to_txt(obsdata)
