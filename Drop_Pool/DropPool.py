# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids

# This is a python script for post-processing of Basilisk C data

# It uses a Basilisk code getData.c (needs to be precompiled)
# It extracts f1 and f2 (water and oil VOF fields in this case)

import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True


def gettingfield(filename):
    print('Getting field values')
    exe = ["./getData", filename, str(xmin), str(xmax), str(ymin), str(ymax), str(nx), str(ny)]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    Xtemp = []
    Ytemp = []
    f1temp = []
    f2temp = []
    for n1 in range(1,len(temp2)):
        temp3 = temp2[n1].split(" ")
        if temp3 == ['']:
            pass
        else:
            Xtemp.append(float(temp3[0]))
            Ytemp.append(float(temp3[1]))
            f1temp.append(float(temp3[2]))
            f2temp.append(float(temp3[3]))
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    f1 = np.asarray(f1temp)
    f2 = np.asarray(f2temp)
    X.resize((nx+1, ny+1))
    Y.resize((nx+1, ny+1))
    f1.resize((nx+1, ny+1))
    f2.resize((nx+1, ny+1))
    print('Got field values')
    return X, Y, f1, f2
# ----------------------------------------------------------------------------------------------------------------------

nGFS = 51

folder = 'Tracer'
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 1.0
Ldomain = 16*d
# These are based on the GFSview coordinates

xmin = -1.0625*d
xmax = 3.9375*d
ymin = 0.0
ymax = 5*d
nx = 640
ny = 640

for ti in range(nGFS):
    t = 1.0 * ti
    place = "intermediate/snapshot-%5.4f" % t
    name = "%s/%4.4d.png" %(folder, ti)
    if not os.path.exists(place):
        print("File not found!")
    else:
        X, Y, f1, f2 = gettingfield(place)

        Xp = Y.transpose()
        Yp = -X.transpose()
        f1 = f1.transpose()
        f2 = f2.transpose()
        ## Part to plot
        fig, ax = plt.subplots()
        fig.set_size_inches(19.20, 10.80)
        rc('axes', linewidth=2)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)

        ax.contourf(Xp, Yp, f1, levels=[0.5, 1.0], colors='blue')
        ax.contourf(Xp, Yp, f2, levels=[0.5, 1.0], colors='red')
        ax.contourf(-Xp, Yp, f1, levels=[0.5, 1.0], colors='blue')
        ax.contourf(-Xp, Yp, f2, levels=[0.5, 1.0], colors='red')

        ax.contour(Xp, Yp, f1, levels=0.5, colors='blue')
        ax.contour(Xp, Yp, f2, levels=0.5, colors='red')
        ax.contour(-Xp, Yp, f1, levels=0.5, colors='blue')
        ax.contour(-Xp, Yp, f2, levels=0.5, colors='red')

        del X
        del Y
        del f1
        del f2

        ax.set_xlabel(r'$X/D$', fontsize=30)
        ax.set_ylabel(r'$Y/D$', fontsize=30)
        plt.axis('square')
        plt.ylim(Yp.min(), Yp.max())
        plt.xlim(-Xp.max(), Xp.max())

        plt.title('t = %5.4f' % t, fontsize=30)
        # plt.show()
        plt.savefig(name)
        plt.close()
        print(("Done %d of %d" % (ti+1, nGFS)))
