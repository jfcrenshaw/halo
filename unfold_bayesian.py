#!/usr/bin/env python

from modules.truth import truth

inputfile = "input.txt"
truth = truth(inputfile) # dictionary of inputs

# Bayesian Unfolding
for config in truth:
	for pair in truth[config]:
		config_num = config[4]
		config_dist = config[6:-3]
		print(config_num,config_dist)
