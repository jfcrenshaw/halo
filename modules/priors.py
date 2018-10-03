#!/usr/bin/env python

import numpy as np
from modules.efficiency_matrix import effmatrix

def prior_positive_plane():

    tru = [[],[]] # array for truth values
    obs = [[],[]] # array for observed values

    for i in range(500):
        for j in range(int(6/8*500+0.5)):
            tru[0].append(i)
            tru[1].append(j)

    M = effmatrix()

    for i in range(len(tru[0])):
        # calculate observations from efficiency matrix
        oneN_obs = tru[0][i]*M.item(0,0)+tru[1][i]*M.item(0,1)
        twoN_obs = tru[0][i]*M.item(1,0)+tru[1][i]*M.item(1,1)
        obs[0].append(oneN_obs)
        obs[1].append(twoN_obs)

    np.save('priors/prior_positive_plane_truth.npy',tru)
    np.save('priors/prior_positive_plane_observed.npy',obs)

def prior_distUnknown():

    tru = [[],[]] # array for truth values
    obs = [[],[]] # array for observed values

    for i in range(500):
        for j in range(int(8./11.*i+0.5)):
            tru[0].append(i)
            tru[1].append(j)
    

    M = effmatrix()

    for i in range(len(tru[0])):
        # calculate observations from efficiency matrix
        oneN_obs = tru[0][i]*M.item(0,0)+tru[1][i]*M.item(0,1)
        twoN_obs = tru[0][i]*M.item(1,0)+tru[1][i]*M.item(1,1)
        obs[0].append(oneN_obs)
        obs[1].append(twoN_obs)

    np.save('priors/prior_distUnknown_truth.npy',tru)
    np.save('priors/prior_distUnknown_observed.npy',obs)


def prior_distKnown(config,dist,dist_uncertainty):

    # create arrays to save numbers to
    oneNtruth = []
    twoNtruth = []
    oneNobs   = []
    twoNobs   = []

    # get the efficiency matrix
    M = effmatrix()

    # Prior envelope
    # the envelope was designed for Halo1, 5kpc but it is easy to rescale for
    # Halo2 and other distances
    # Halo1 -> Halo2: mass of Halo2 / mass of Halo1 = 1000/79 = config_scale
    # distance factor = (5kpc/distance)^2
    # BUT there are 2 distances here: distance+uncert and distance-uncert
    distc = dist*(1.-dist_uncertainty) # closer dist
    distf = dist*(1.+dist_uncertainty) # farther dist
    scalec = (5.0/distc)**2
    scalef = (5.0/distf)**2
    if config == 2:
        scalec /= 0.079
        scalef /= 0.079


    # The prior --------------------------------------------------------
    # points for the envelope
    # point 0       1          2          3          4
    X = [8.*scalef,125.*scalec,85.*scalec,45.*scalef,8.*scalef]
    Y = [0.,       30.*scalec, 63.*scalec,31.*scalef,1.       ]

    # points 0 and 1 are connected by a polynomial of order 1.7: 
    # y1=A*(x1-x0)^1.7+y0
    def f01(x):
        A = (Y[1]-Y[0])*(X[1]-X[0])**(-1.7)
        return A*(x-X[0])**(1.7)+Y[0]

    # points 1 and 2 are connected by a line
    def f12(x):
        B = (Y[2]-Y[1])/(X[2]-X[1])
        return B*(x-X[1])+Y[1]

    # points 2 and 3 are connected by a line
    def f23(x):
        C = (Y[3]-Y[2])/(X[3]-X[2])
        return C*(x-X[2])+Y[2]

    # points 3 and 4 are connected by a quadratic:
    # y3=D*(x3-x4)^2+y4
    def f34(x):
        D = (Y[3]-Y[4])*(X[3]-X[4])**(-2)
        return D*(x-X[4])**2+Y[4]

    for oneN in range(int(X[0]),int(X[1])+1):

        # determine the range for twoN based on the current oneN
        y_lo = 0
        y_hi = -1
        if oneN >= X[0] and oneN < X[3]:
            y_lo = int(f01(oneN))
            y_hi = int(f34(oneN))
        elif oneN >= X[3] and oneN < X[2]:
            y_lo = int(f01(oneN))
            y_hi = int(f23(oneN))
        elif oneN >= X[2] and oneN <= X[1]:
            y_lo = int(f01(oneN))
            y_hi = int(f12(oneN))

        # iterate through twoN
        for twoN in range(y_lo,y_hi+1):

            oneNtruth.append(oneN)
            twoNtruth.append(twoN)

            # Calculate observations
            oneNobs.append(M.item(0,0)*oneN + M.item(0,1)*twoN)
            twoNobs.append(M.item(1,0)*oneN + M.item(1,1)*twoN)

    # save arrays to files
    tru = [oneNtruth,twoNtruth]
    obs = [oneNobs,twoNobs]
    prior_location = './priors/'
    fname = prior_location+'prior_halo'+str(config)+'_'+str(int(dist))+'kpc'
    np.save(fname+'_truth.npy',tru)
    np.save(fname+'_observed.npy',obs)