#!/usr/bin/env python

# This script takes distance and eff as inputs, and creates an efficiency matrix,
# the truth prior, the observed prior, and the observed distribution

import numpy as np

# ------------------------------------------------------------------------------
# Main function ----------------------------------------------------------------
# ------------------------------------------------------------------------------

config = 1 # 1=HALO, 2=HALO-1kT
dist_uncertainty = [0,0.1,0.2,0.3,0.4,0.5]
dist = [2,4,6,8] # supernova distance in kpc
eff = [0.28] # 1n detection efficiency

def main():
    for d in dist:
        for du in dist_uncertainty: 

            # distance known prior
            prior_distKnown(config,d,du,eff)

            for e in eff:

                simulate_observations(config,d,e)


# ------------------------------------------------------------------------------
# Distance Known Figure of Merit -----------------------------------------------
# ------------------------------------------------------------------------------

def prior_distKnown(config,dist,dist_uncertainty,eff):

    # create arrays to save numbers to
    oneNtruth = []
    twoNtruth = []

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
            #oneNobs.append(M.item(0,0)*oneN + M.item(0,1)*twoN)
            #twoNobs.append(M.item(1,0)*oneN + M.item(1,1)*twoN)

    # save truth to file
    tru = [oneNtruth,twoNtruth]
    prior_location = './priors/'
    fname = prior_location+'prior_halo'+str(config)+'_'+str(int(dist))+'kpc'+\
            '_distUncert'+str(int(100*dist_uncertainty))
    np.save(fname+'_truth.npy',tru)
    
    # save observed priors
    for e in eff:

        M = np.matrix([[e,2*e*(1-e)],[0,e**2]])

        oneNobs   = []
        twoNobs   = []
        for i in range(len(oneNtruth)):
            oneN = oneNtruth[i]
            twoN = twoNtruth[i]
            oneNobs.append(M.item(0,0)*oneN + M.item(0,1)*twoN)
            twoNobs.append(M.item(1,0)*oneN + M.item(1,1)*twoN)
        obs = [oneNobs,twoNobs]
        np.save(fname+'_observed_E'+str(int(e*100))+'.npy',obs)


# ------------------------------------------------------------------------------
# Calculate Observed Distribution ----------------------------------------------
# ------------------------------------------------------------------------------

def simulate_observations(config,dist,e):

    # efficiency matrix
    M = np.matrix([[e,2*e*(1-e)],[0,e**2]])

    scale = (5.0/dist)**2
    if config == 2:
        scale /= 0.079

    oneN = 72*scale
    twoN = 48*scale

    tru = [[],[]] # array for truth values
    obs = [[],[]] # array for observed values

    ntrials = 10000 # how many trials to run
    for i in range(ntrials):

        truth_1n = np.random.poisson(oneN)
        truth_2n = np.random.poisson(twoN)

        # calculate observed numbers
        observed = [0.0,0.0]
        for j in range(truth_1n):
            rand = np.random.uniform(0,1)
            if rand <= M.item(0,0):
                observed[0] += 1.0
            elif rand > M.item(0,0) and rand <= M.item(0,0) + M.item(1,0):
                observed[1] += 1.0
        for j in range(truth_2n):
            rand = np.random.uniform(0,1)
            if rand <= M.item(0,1):
                observed[0] += 1.0
            elif rand > M.item(0,1) and rand <= M.item(0,1) + M.item(1,1):
                observed[1] += 1.0

        # add the truth and observed to the master list
        tru[0].append(truth_1n)
        tru[1].append(truth_2n)
        obs[0].append(observed[0])
        obs[1].append(observed[1])

        # Save the file for this config/pair
        data_location = './data/'
        output_truth = 'halo'+str(config)+'_'+str(dist)+'kpc_truth_E'+str(int(e*100))+'.npy'
        output_obs = 'halo'+str(config)+'_'+str(dist)+'kpc_observed_E'+str(int(e*100))+'.npy'
        #np.save(data_location+output_truth,tru)
        np.save(data_location+output_obs,obs)


main()