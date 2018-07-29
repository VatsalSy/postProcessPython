# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids

import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True


def gettingfield(t):
    print('Getting field values')
    name = 'OutputData/%5.4f.txt' % t
    f = open(name, "r")
    temp1 = f.read()
    f.close()
    temp2 = temp1.split("\n")
    Xtemp = []
    Ytemp = []
    f1temp = []
    f2temp = []
    Utemp = []
    Vtemp = []
    for n1 in range(1, len(temp2) - 1):
        temp3 = temp2[n1].split(" ")
        Xtemp.append(float(temp3[0]))
        Ytemp.append(float(temp3[1]))
        f1temp.append(float(temp3[2]))
        f2temp.append(float(temp3[3]))
        Utemp.append(float(temp3[4]))
        Vtemp.append(float(temp3[5]))
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    f1 = np.asarray(f1temp)
    f2 = np.asarray(f2temp)
    U = np.asarray(Utemp)
    V = np.asarray(Vtemp)
    X.resize((ny, nx))
    Y.resize((ny, nx))
    f1.resize((ny, nx))
    f2.resize((ny, nx))
    U.resize((ny, nx))
    V.resize((ny, nx))
    return X, Y, f1, f2, U, V
    print('Got field values')

# ----------------------------------------------------------------------------------------------------------------------


nGFS = 1
tmp = np.ones(nGFS)

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)
d = 2*1e-3
# notice that the number of elements in y and x are different than that used for
# basilisk interpretation. Because of change from GFSvariable
ny = 500
nx = 1000

for ti in range(nGFS):
    t = 0.0005 * ti
    X, Y, f1, f2, U, V = gettingfield(t)
    name = "%s/%4.4d.png" %(folder, ti)
    fig, ax = plt.subplots()
    fig.set_size_inches(19.20, 10.80)
    rc('axes', linewidth=2)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    speed = np.sqrt(U**2 + V**2)
    maxs = speed.max()
    if maxs > 0:
        U /= maxs
        V /= maxs
        speed /= maxs
    ax.streamplot(X[0,:], -Y[:,0], U, -V, density = 6, color = speed, linewidth=1, cmap='Greys')
    ax.contourf(X, Y, f1, levels=[0.5, 1.0], colors='blue',alpha=0.70)
    ax.contourf(X, Y, f2, levels=[0.5, 1.0], colors='red',alpha=0.70)
    ax.contour(X, Y, f1, levels=0.5, colors='blue')
    ax.contour(X, -Y, f1, levels=0.5, colors='blue')
    ax.contour(X, Y, f2, levels=0.5, colors='red')
    ax.contour(X, -Y, f2, levels=0.5, colors='red')
    ax.set_xlabel(r'$X/D$', fontsize=30)
    ax.set_ylabel(r'$Y/D$', fontsize=30)
    plt.axis('equal')
    plt.xlim(X.min(), X.max())
    plt.ylim(-Y.max(), Y.max())
    plt.title('t = %5.4f s' % t, fontsize=30)
    # plt.show()
    plt.savefig(name)
    plt.close()
    print(("Done %d of %d" % (ti+1, nGFS)))
