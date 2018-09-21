#!/usr/bin/env python

import numpy as np

from modules.truth import truth
from modules.prior_distUnknown import prior_distUnknown
from modules.prior_distKnown import prior_distKnown

inputfile = 'input.txt'
truth = truth(inputfile)

dist_uncertainty = 0.1

#prior_distUnknown()

for config in truth:
    config_ = int(config[4])
    dist = float(config[6:-3])
    prior_distKnown(config_,dist,dist_uncertainty)