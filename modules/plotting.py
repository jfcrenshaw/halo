import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.interpolate import Rbf

# This module contains a suite of functions that are used to make the contour
# plots of the unfolded data. The first two are for 'smearing' the data so a 
# contour can be applied. The third makes the contour plot. The fourth makes a
# scatter plot. The fifth is a function to pre-process data sets where 2n = 0.



# kernal density estimation to be used for making contours
def kde(m1,m2,xmin,xmax,ymin,ymax,xres,yres):
    # kernal density estimation. This is used to 'smear' the data and assign
    # a function z = f(oneN,twoN) so that a contour can be made.
    # This function is used inside the density_cut function.

    # create a grid of points to sample from. xres and yres determine the
    # spacing of sample points. Lower xres and yres mean greater 'smearing'
    X, Y = np.mgrid[xmin:xmax:xres, ymin:ymax:yres]
    positions = np.vstack([X.ravel(), Y.ravel()])                                                       
    values = np.vstack([m1, m2])
    # do a gaussian kernal density estimation                                                                        
    kernel = stats.gaussian_kde(values)                                                                 
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z



def density_cut(oneN,twoN,xmin,xmax,ymin,ymax,xres,yres,cut=0.1,trim=False):
    # This function does a kde of the data (see the previous function), then
    # interpolates it so it can be applied to the data points (oneN,twoN). It
    # then calculates a z for every oneN,twoN pair, and calculates a cut on z
    # that excludes a certain fraction of data points (normally 1/10).
    # If trim == False, it returns the x,y,z values from the kde, and the
    # appropriate cut on z. If trim == true, it returns the list of oneN,twoN
    # values that passed the cut on z.

    # kernal density estimation (see previous function)
    X,Y,Z = kde(oneN,twoN,xmin,xmax,ymin,ymax,xres,yres)
    # interpolate
    f = Rbf(X,Y,Z)
    # calculate z values for data points
    zi = f(oneN,twoN)
    # put them in order least to greatest
    zi.sort()
    # apply a cut that will remove a fraction of the data
    cut_index = int(cut*len(oneN))-1
    if cut_index >= 0:
        cut_ = zi[cut_index]
    else:
        cut_ = zi[0]

    # if trim == false, return the X,Y,Z from the kde, and the cut
    if trim == False:
        return X,Y,Z,cut_

    # if trim == true, return the trimmed data set
    else:
        oneN_ = []
        twoN_ = []
        for i in range(len(oneN)):
            if f(oneN[i],twoN[i]) >= cut_:
                oneN_.append(oneN[i])
                twoN_.append(twoN[i])
            
        return oneN_,twoN_



def contours(X,Y,Z,cut,ax):
    # This function plots the contours, given the x,y,z and cut from the 
    # density_cut function (see above).
    
    # invisible 'color' for the unwanted contour levels
    invis = [0,0,0,0]

    # plot the contours -----
    # gray fill
    levels = [0,cut,1]
    ax.contourf(X,Y,Z,levels=levels,colors=[invis,'0.9',invis],zorder=1)
    # black outline
    ax.contour(X,Y,Z,levels=cut,colors='black',linewidths=0.8,zorder=10)

    # axis labels
    ax.set_xlabel('1n events',horizontalalignment='right',x=1.0)
    ax.set_ylabel('2n events',horizontalalignment='right', y=1.0)


def scatter(X,Y,ax):
    # This function plots a scatter plot y vs x on axis ax.
    # Very simple, but obviates the need to set the marker and axis labels
    # every time.
    ax.scatter(X,Y,marker='.')
    ax.set_xlabel('1n events',horizontalalignment='right',x=1.0)
    ax.set_ylabel('2n events',horizontalalignment='right', y=1.0)   



def zero_fix(oneN,twoN):
    # The kde has problems with data sets where every 2n = 0. This is because
    # the variance = 0, which results in a divison by zero at some point in the
    # algorithm.
    # To avoid this issue, this function changes half of the 2n's to 1.
    # It also removes 10% of the data so we don't have to worry about it later.

    xvals = set(oneN)
    xdict = dict()
    for i in xvals:
        xdict[i] = 0
        
    for i in oneN:
        xdict[i] += 1
    
    xvals   = []
    xweight = []
    for i in xdict:
        xvals.append(i)
        xweight.append(xdict[i])
        
    while sum(xweight) > 0.9*len(oneN):
        min_index = np.argmin(xweight)
        del xvals[min_index]
        del xweight[min_index]
    
    oneN_ = []
    twoN_ = []
    for i in range(len(xweight)):
        for j in range(xweight[i]):
            oneN_.append(xvals[i])
            if j % 2 == 0:
                twoN_.append(0)
            else:
                twoN_.append(1)
            
    return oneN_,twoN_

        