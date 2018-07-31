#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


def snowglobes_curves(axis,detector,dist,color):

    # Load all the data --------------------------------------------------------
    sn_model_location = './sn_flux_models/'

    E13L1NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=13.0_Lnux=1.0_NH.txt',unpack=True) 
    E18L1NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=18.0_Lnux=1.0_NH.txt',unpack=True)
    E25L1NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=25.0_Lnux=1.0_NH.txt',unpack=True)

    E13L1IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=13.0_Lnux=1.0_IH.txt',unpack=True)  
    E18L1IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=18.0_Lnux=1.0_IH.txt',unpack=True)
    E25L1IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=25.0_Lnux=1.0_IH.txt',unpack=True) 

    E13L2NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=13.0_Lnux=2.0_NH.txt',unpack=True)
    E18L2NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=18.0_Lnux=2.0_NH.txt',unpack=True)
    E25L2NH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=25.0_Lnux=2.0_NH.txt',unpack=True)

    E13L2IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=13.0_Lnux=2.0_IH.txt',unpack=True)
    E18L2IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=18.0_Lnux=2.0_IH.txt',unpack=True)
    E25L2IH = np.genfromtxt(sn_model_location+
                'neutron_numbers_Enux=25.0_Lnux=2.0_IH.txt',unpack=True)
    #---------------------------------------------------------------------------

    # Note: the snowglobes curves were calculated for HALO2 at 10kpc
    # need to be rescaled if used for HALO1 or 5kpc
    scale = 1
    if detector == 1:
        scale *= 0.079
    scale *= (10.0/dist)**2


    if color == True:
        colors = ['r','b']
    else:
        colors = ['black','black']

    for i in [E13L1NH,E18L1NH,E25L1NH]:
        axis.plot(i[0]*scale,i[1]*scale,color=colors[0],linestyle='--')
    for i in [E13L1IH,E18L1IH,E25L1IH]:
        axis.plot(i[0]*scale,i[1]*scale,color=colors[0],linestyle='-')
    for i in [E13L2NH,E18L2NH,E25L2NH]:
        axis.plot(i[0]*scale,i[1]*scale,color=colors[1],linestyle='--')
    for i in [E13L2IH,E18L2IH,E25L2IH]:
        axis.plot(i[0]*scale,i[1]*scale,color=colors[1],linestyle='-')

