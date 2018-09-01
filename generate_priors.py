#!/usr/bin/env python

import numpy as np

from modules.truth import truth
from modules.prior_distUnknown import prior_distUnknown

inputfile = 'input.txt'
truth = truth(inputfile)

dist_uncertainty = 0.1

prior_distUnknown()
