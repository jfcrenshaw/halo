#!/usr/bin/env python

import numpy as np 

def other_sn_models(axis,detector,dist,color):

    sn_model_location = './sn_flux_models/'

    # Get Huedepohl points
    NHoneN,NHtwoN,IHoneN,IHtwoN = np.genfromtxt(sn_model_location+'Huedepohl.txt',
                                    skip_header=12,usecols=(1,2,3,4),unpack=True)

    # Get other points

    other1nNH,other2nNH,other1nIH,other2nIH = np.genfromtxt(sn_model_location+'other_models.txt',
                                                    skip_header=5,usecols=(1,2,3,4),unpack=True)


    # Note: snowglobes values were calculated for HALO2 at 10kpc
    # need to be rescaled if used for HALO1 or 5kpc
    scale = 1
    if detector == 1:
        scale *= 0.079
    scale *= (10.0/dist)**2

    # Huedepohl points
    half = len(NHoneN)//2
    if color == True:
        LSS20_color = 'black'
        shen_color = 'silver'
    elif color == False:
        LSS20_color = 'black'
        shen_color = 'black'
    else:
        LSS20_color = color
        shen_color = color

    axis.scatter(NHoneN[:half]*scale,NHtwoN[:half]*scale,marker='s',edgecolors=LSS20_color,facecolors='none')
    axis.scatter(IHoneN[:half]*scale,IHtwoN[:half]*scale,marker='s',color=LSS20_color)
    axis.scatter(NHoneN[half:]*scale,NHtwoN[half:]*scale,marker='s',edgecolors=shen_color,facecolors='none')
    axis.scatter(IHoneN[half:]*scale,IHtwoN[half:]*scale,marker='s',color=shen_color)

    # Other points
    if color == True:
        colors = ['c','m','forestgreen']
    elif color == False:
        colors = ['black','black','black']
    else:
        colors = [color,color,color]

    for i in range(len(other1nNH)):
        axis.scatter(other1nNH[i]*scale,other2nNH[i]*scale,marker='s',edgecolors=colors[i],facecolors='none')
        axis.scatter(other1nIH[i]*scale,other2nIH[i]*scale,marker='s',color=colors[i])