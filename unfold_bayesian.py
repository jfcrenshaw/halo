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

		# observed data
		obsdata  = './data/halo'+str(config_num)+'_'+str(config_dist)+'kpc_'+\
					str(oneN)+'v'+str(twoN)+'_observed.npy'

		# save a txt version for root to use
		npy_to_txt(obsdata)

		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------
		# UNFOLD WITH THE POSITIVE PLANE PRIOR
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------

		# prior names
		if config[:5] == 'halo1':
			truprior = './priors/prior_positive_plane_truth.npy'
			obsprior = './priors/prior_positive_plane_observed.npy'
		elif config[:5] == 'halo2':
			truprior = './priors/prior_halo2_positive_plane_truth.npy'
			obsprior = './priors/prior_halo2_positive_plane_observed.npy'

		# save text versions
		npy_to_txt(truprior)
		npy_to_txt(obsprior)

		# Unfold
		os.system("root -l -q 'modules/unfold_bayesian_root.C({0},{1},{2},{3},{4} \
					)'".format(config_num,config_dist,oneN,twoN,1))
		
		# save the unfolded text file as npy file
		unfolded  = './unfolded_data/halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_'+str(oneN)+'v'+str(twoN)+'_unfolded_bayesian_PP.txt'
        	txt_to_npy(unfolded)
		
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------
		# UNFOLD WITH THE DISTANCE UNKNOWN PRIORS
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------

		# prior names
		if config[:5] == 'halo1':
			truprior = './priors/prior_distUnknown_truth.npy'
			obsprior = './priors/prior_distUnknown_observed.npy'
		if config[:5] == 'halo2':
			truprior = './priors/prior_halo2_distUnknown_truth.npy'
			obsprior = './priors/prior_halo2_distUnknown_observed.npy'

		# save text versions
		npy_to_txt(truprior)
		npy_to_txt(obsprior)

		# Unfold
		os.system("root -l -q 'modules/unfold_bayesian_root.C({0},{1},{2},{3},{4} \
					)'".format(config_num,config_dist,oneN,twoN,2))
		
		# save the unfolded text file as npy file
		unfolded  = './unfolded_data/halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_'+str(oneN)+'v'+str(twoN)+'_unfolded_bayesian_'+\
					'distUnknown.txt'
        	txt_to_npy(unfolded)

		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------
		# UNFOLD WITH THE DISTANCE KNOWN PRIORS
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------

		# prior names
		truprior = './priors/prior_halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_truth.npy'
		obsprior = './priors/prior_halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_observed.npy' 

		# save text versions
		npy_to_txt(truprior)
		npy_to_txt(obsprior)
		npy_to_txt(obsdata)

		# Unfold
		os.system("root -l -q 'modules/unfold_bayesian_root.C({0},{1},{2},{3},{4} \
					)'".format(config_num,config_dist,oneN,twoN,3))

		# save the unfolded text file as npy file
		unfolded  = './unfolded_data/halo'+str(config_num)+'_'+str(config_dist)+\
					'kpc_'+str(oneN)+'v'+str(twoN)+'_unfolded_bayesian_'+\
					'distKnown.txt'
        	txt_to_npy(unfolded)
		
	
		# ----------------------------------------------------------------------
		# ----------------------------------------------------------------------

		# remove the text files
		os.system('rm data/*txt')
		os.system('rm priors/*txt')
       		os.system('rm unfolded_data/*txt')




