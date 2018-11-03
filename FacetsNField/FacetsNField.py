# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
# This file imports field data (see gettingfield) and 
# facets (see gettingfacets)

import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True

def gettingFacets(filename):
    print('Getting facets values')
    exe = ["./getFacet", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    Xtemp = []
    Ytemp = []
    for n1 in range(len(temp2)):
        temp3 = temp2[n1].split(" ")
        if temp3 == ['']:
            pass
        else:
            Xtemp.append(float(temp3[0]))
            Ytemp.append(float(temp3[1]))
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    print('Got facets values')
    return X, Y


def gettingfield(filename):
    print('Getting field values')
    exe = ["./getData", filename, str(LEVEL)]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    Xtemp = []
    Ytemp = []
    D2temp = []
    for n1 in range(1,len(temp2)):
        temp3 = temp2[n1].split(" ")
        if temp3 == ['']:
            pass
        else:
            Xtemp.append(float(temp3[0]))
            Ytemp.append(float(temp3[1]))
            D2temp.append(float(temp3[2]))
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    D2 = np.asarray(D2temp)

    N = 2**LEVEL
    X.resize((N+1, N+1))
    Y.resize((N+1, N+1))
    D2.resize((N+1, N+1))

    print('Got field values')
    return X, Y, D2

# ----------------------------------------------------------------------------------------------------------------------
R = 0.1

nGFS = 100
dt = 0.01

xmin1 = 0.0
xmax1 = 10.0
ymin1 = 0.0
ymax1 = 10.0

xmin2 = 0.0
xmax2 = 1.1
ymin2 = 0.0
ymax2 = 1.1

LEVEL = 9

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

for ti in range(nGFS):
    t = dt*ti
    place = "intermediate/snapshot-%5.4f" % t
    name = "%s/%4.4d.png" %(folder, ti)

    Xf, Yf = gettingFacets(place)
    Xf /= R
    Yf /= R

    X, Y, D2 = gettingfield(place)
    X /= R
    Y /= R
    if D2.max() > 0:
        D2 = np.log(D2)/np.log(10)
    else:
        D2 = -10*np.ones((len(D2),len(D2[0])))

    ## Part to plot
    plt.close()
    fig, (ax2, ax1) = plt.subplots(1, 2, sharey=False)
    fig.set_size_inches(19.20, 10.80)
    time = t*25
    fig.suptitle(r'\textbf{t = %2.1f}' % time, fontsize=30)
    rc('axes', linewidth=2)

    ## Drawing Facets
    for i in range(0,len(Xf),2):
        ax2.plot([Xf[i], Xf[i+1]],[Yf[i], Yf[i+1]],'-',color='black',linewidth=3)
    ## D2
    # cntrl = ax.pcolormesh(X, Y, D2, cmap="RdBu_r",edgecolor='face', vmax = D2.max(), vmin = D2.min())
    cntrl = ax2.imshow(D2.transpose(), interpolation='bilinear', cmap="RdBu_r",
               origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()],
               vmax=1, vmin=-5)
    ax2.set_xlabel(r'$X/D$', fontsize=30,labelpad=30)
    ax2.set_ylabel(r'$Y/D$', fontsize=30)
    ax2.set_aspect('equal')
    ax2.set_ylim(xmin2, xmax2)
    ax2.set_xlim(ymin2, ymax2)
    ax2.xaxis.set_tick_params(labelsize=25)
    ax2.xaxis.tick_top()
    ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_tick_params(labelsize=25)

    ## Drawing Facets
    for i in range(0,len(Xf),2):
        ax1.plot([Xf[i], Xf[i+1]],[Yf[i], Yf[i+1]],'-',color='black',linewidth=3)
    ## D2
    # cntrl = ax.pcolormesh(X, Y, D2, cmap="RdBu_r",edgecolor='face', vmax = D2.max(), vmin = D2.min())
    cntrl = ax1.imshow(D2.transpose(), interpolation='bilinear', cmap="RdBu_r",
               origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()],
               vmax=1, vmin=-5)
    cb1 = fig.add_axes([0.10, 0.10, 0.80, 0.05])
    c1 = plt.colorbar(cntrl,cax=cb1, orientation='horizontal')
    c1.set_label(r'$log_{10}\left(\|D_{ij}\|\right)$', fontsize=30,labelpad=12)
    c1.ax.tick_params(labelsize=20)
    c1.ax.tick_params(labelbottom=True)

    ax1.set_xlabel(r'$X/D$', fontsize=30,labelpad=30)
    ax1.set_ylabel(r'$Y/D$', fontsize=30)
    ax1.set_aspect('equal')
    ax1.set_ylim(xmin1, xmax1)
    ax1.set_xlim(ymin1, ymax1)
    ax1.xaxis.set_tick_params(labelsize=25)
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.yaxis.set_tick_params(labelsize=25)


    print(("Done %d of %d" % (ti+1, nGFS)))
    # plt.show()
    plt.savefig(name)
    plt.close()
