# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids

# For some reason, python plotting (because of for loop) is really slow
# Use MATLAB as then no need to take care of for loop

import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
import time

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True

def gettingCells(filename):
    print('Getting Cells values')
    exe = ["./getCells", filename]
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
    print('Got Cells values')
    return X, Y


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

# ----------------------------------------------------------------------------------------------------------------------

nGFS = 2
dt = 0.01
xmin = 0.0
xmax = 1.0
ymin = 0.0
ymax = 1.0
LEVEL = 9

folder = 'Grid'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)
for ti in range(1,nGFS):
    t = ti*dt
    place = "intermediate/snapshot-%5.4f" % t
    name = "grid%6.6d.eps" % ti

    Xf, Yf = gettingFacets(place)
    Xg, Yg = gettingCells(place)

    tstart = time.time()
    ## Part to plot
    plt.close()
    fig, ax = plt.subplots()
    fig.set_size_inches(9.40, 9.40)
    rc('axes', linewidth=2)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    Xg.resize((int(len(Xg)/5),5))
    Yg.resize((int(len(Yg)/5),5))
    for i in range(0,len(Xg)):
        ax.plot(Xg[i,1:5],Yg[i,1:5],'-',color='grey',linewidth=1)
    ## Drawing Facets
    for i in range(0,len(Xf),2):
        ax.plot([Xf[i], Xf[i+1]],[Yf[i], Yf[i+1]],'-',color='black',linewidth=3)
    # ax.plot(Xg, Yg,'.',color='black',linewidth=3)

    ax.set_xlabel(r'$X$', fontsize=30)
    ax.set_ylabel(r'$Y$', fontsize=30)
    ax.set_aspect('equal')
    ax.set_ylim(xmin, xmax)
    ax.set_xlim(ymin, ymax)
    ax.set_title(r'\textbf{t = %2.1f}' % t, fontsize=30)
    print('Time:', (time.time()-tstart))
    print("Done")
    # plt.show()
    plt.savefig(name)
    plt.close()
