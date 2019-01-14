import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# This module contains a suite of functions that are used to make the contour
# plots of the unfolded data..

def trim_data(xdata,ydata,percent=0.1):
    
    npoints = len(xdata)

    values = np.vstack([xdata,ydata])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(values).T,xdata.shape)
    
    sort = [i for i in Z]
    sort.sort()
    cut = sort[int(percent*npoints+0.5)]
    
    xcut = []
    ycut = []
    for i in range(npoints):
        if Z[i] >= cut:
            xcut.append(xdata[i])
            ycut.append(ydata[i])
    
    return np.array(xcut),np.array(ycut),cut



# We need a special function for the cases where 2n = 0 for every point
# this is because the variance of 2n is 0, which messes up the KDE
# What we do is a 1D KDE for the 1D data, remove 10% of the data, then generate
# a gaussian distribution of 2n points for these 1n points
# we then do the normal KDE on these points to determine the cut
def trim_data_2n0(xdata):

    # 1D KDE ------------------------------------
    npoints = len(xdata)

    kernel = stats.gaussian_kde(xdata)
    Z = kernel(xdata)
    sort = [i for i in Z]
    sort.sort()
    cut = sort[int(0.1*npoints)]

    xcut = []
    for i in range(npoints):
        if Z[i] >= cut:
            xcut.append(xdata[i])
    xcut = np.array(xcut)
    # ------------------------------------------

    # gaussian distribution of 2n --------------
    ycut = []
    for i in range(len(xcut)):
        ycut.append(np.random.normal(loc=0,scale=0.5))
    # ------------------------------------------

    # 2D KDE of 2n,1n --------------------------
    values = np.vstack([xcut,ycut])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(values).T,xcut.shape)
    cut = min(Z)

    return np.array(xcut),np.array(ycut),cut



# Define colors for the contours below
GRAY = sns.light_palette('lightgray',n_colors=1,as_cmap=True)
BLACK = sns.dark_palette('black',n_colors=1,as_cmap=True)

# This function plots the contours given the data and the cut from the kde
def contours(X, Y, cut, ax, x_bw=False, y_bw=False, gridsize=200):

    # default bandwidths
    if x_bw == False:
        x_bw = np.std(X)/3
    if y_bw == False:
        y_bw = np.std(Y)/2

    # filled contour
    sns.kdeplot(X,Y,n_levels=[0,cut,1],shade=True,shade_lowest=False,cmap=GRAY,
                                        bw=[x_bw,y_bw],gridsize=gridsize,ax=ax)
    # contour outline
    sns.kdeplot(X,Y,n_levels=[0,cut,1],cmap=BLACK,bw=[x_bw,y_bw],
                                                        gridsize=gridsize,ax=ax)
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
