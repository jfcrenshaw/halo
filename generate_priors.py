#!/usr/bin/env python

import numpy as np

from modules.truth import truth
from modules.priors import prior_positive_plane, prior_distUnknown, prior_distKnown

inputfile = 'input.txt'
truth = truth(inputfile)

dist_uncertainty = 0.1

# generate positive plane prior
prior_positive_plane()

# generate the distance unknown prior
prior_distUnknown()

# generate the distance known priors
for config in truth:
    config_ = int(config[4])
    dist = float(config[6:-3])
    prior_distKnown(config_,dist,dist_uncertainty)
