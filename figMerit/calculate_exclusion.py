#!/usr/bin/env python

import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


config = 1 # 1=HALO, 2=HALO-1kT
dist_uncertainty = [0,0.1,0.2,0.3,0.4,0.5]
dist = [2,4,6,8] # supernova distance in kpc
eff = [0.28] # 1n detection efficiency


def main():

    outfile = open('exclusions.txt','w')
    outfile.write('{0:<15}{1:<15}{2:<8}{3:<15}\n'.format('Dist (kpc)','Dist Uncert','Eff','Exclusion')) 

    for d in dist:
        for du in dist_uncertainty:
            for e  in eff:

                # load the unfolded data
                file = 'unfolded_data/halo'+str(config)+'_'+str(d)+\
                        'kpc_distUncert'+str(int(100*du))+'_unfolded_E'+\
                        str(int(100*e))+'.npy'
                oneN,twoN = np.load(file)

                # trim data and form contour
                x,y,cut = trim_data(oneN,twoN)
                ax = plt.axes()
                cs = contours(x,y,cut,ax)

                # calculate contour area
                # get the vertices
                p = cs.collections[0].get_paths()[0]
                x = p.vertices[:,0]
                y = p.vertices[:,1]
                # area with Green's theorem
                area = 0.5*np.sum(y[:-1]*np.diff(x) - x[:-1]*np.diff(y))
                area = np.abs(area)
                
                # load the prior data
                prior = 'priors/prior_halo'+str(config)+'_'+str(d)+'kpc'+\
                        '_distUncert'+str(int(100*du))+'_truth.npy'
                oneN,twoN = np.load(prior)
                prior_area = len(oneN)

                Exclusion = 1-area/prior_area

                outfile.write('{0:<15}{1:<15}{2:<8}{3:<15}\n'.format(d,du,e,Exclusion))

                ax.remove()


def trim_data(xdata,ydata):
    
    npoints = len(xdata)

    values = np.vstack([xdata,ydata])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(values).T,xdata.shape)
    
    sort = [i for i in Z]
    sort.sort()
    cut = sort[int(0.1*npoints)]
    
    xcut = []
    ycut = []
    for i in range(npoints):
        if Z[i] >= cut:
            xcut.append(xdata[i])
            ycut.append(ydata[i])
    
    return np.array(xcut),np.array(ycut),cut


BLACK = sns.dark_palette('black',n_colors=1,as_cmap=True)
# This function plots the contours given the data and the cut from the kde
def contours(X, Y, cut, ax, x_bw=False, y_bw=False, gridsize=200):

    # default bandwidths
    if x_bw == False:
        x_bw = np.std(X)/3
    if y_bw == False:
        y_bw = np.std(Y)/2

    # contour outline
    cs = sns.kdeplot(X,Y,n_levels=[0,cut,1],cmap=BLACK,bw=[x_bw,y_bw],
                                                        gridsize=gridsize,ax=ax)
    # axis labels
    ax.set_xlabel('1n events',horizontalalignment='right',x=1.0)
    ax.set_ylabel('2n events',horizontalalignment='right', y=1.0)
    
    return cs


main()