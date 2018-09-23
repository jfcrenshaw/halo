#!/usr/bin/env python

# This module converts numpy arrays to a normal text file so that they can
# be read in for ROOT, and vice versa

import numpy as np 

def npy_to_txt(filename):

    oneN, twoN = np.load(filename)
    txtfile = open(filename[:-3]+'txt','w')

    for i in range(len(oneN)):
        txtfile.write('{0:<8}{1}\n'.format(oneN[i],twoN[i]))

def txt_to_npy(filename):

    oneN, twoN = np.genfromtxt(filename,unpack=True)
    save_array = [oneN,twoN]
    np.save(filename[:-3]+'npy',save_array)

