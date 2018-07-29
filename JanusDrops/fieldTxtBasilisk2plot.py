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


def gettingfield(t,n):
    print('Getting field values')
    name = 'intermediate/snapshot-%5.4f.txt' % t
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
        if temp3 == ['']:
            pass
        else:
            if (float(temp3[0]) >= xmin and float(temp3[0]) <= xmax and float(temp3[1]) >= ymin and float(temp3[1]) <= ymax):
                Xtemp.append(float(temp3[0]))
                Ytemp.append(float(temp3[1]))
                f1temp.append(float(temp3[2]))
                f2temp.append(float(temp3[3]))
                Utemp.append(float(temp3[4]))
                Vtemp.append(float(temp3[5]))
                #print(temp3[1])
            else:
                Xtemp.append(float(temp3[0]))
                Ytemp.append(float(temp3[1]))
                f1temp.append(0.0)
                f2temp.append(0.0)
                Utemp.append(0.0)
                Vtemp.append(0.0)
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    f1 = np.asarray(f1temp)
    f2 = np.asarray(f2temp)
    U = np.asarray(Utemp)
    V = np.asarray(Vtemp)
    X.resize((n, n))
    Y.resize((n, n))
    f1.resize((n, n))
    f2.resize((n, n))
    U.resize((n, n))
    V.resize((n, n))
    return X, Y, f1, f2, U, V
    print('Got field values')

# ----------------------------------------------------------------------------------------------------------------------


nGFS = 1
tmp = np.ones(nGFS)

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)
d = 2*1e-3
MAXlevel = 8
n = 2**MAXlevel + 1
Ldomain = 8*d
xmin = -0.25*Ldomain
xmax = 0.25*Ldomain
ymin = 0.0*Ldomain
ymax = 1.5*d

for ti in range(nGFS):
    t = 0.0005 * ti
    X, Y, f1, f2, U, V = gettingfield(t,n)
    xtemp = []
    ytemp = []
    for i in range(n):
        xtemp.append(X[i,0])
        ytemp.append(Y[0,i])
    x = np.asarray(xtemp)
    y = np.asarray(ytemp)
    name = "%s/%4.4d.png" %(folder, ti)
    fig, ax = plt.subplots()
    fig.set_size_inches(19.20, 10.80)
    rc('axes', linewidth=2)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    speed = np.sqrt(U**2 + V**2)
    maxs = speed.max()
    speed /= maxs
    ax.streamplot(X[:,0]/d, -Y[0,:]/d, U.transpose()/maxs, -V.transpose()/maxs, density = 6, color = speed.transpose(), linewidth=2, cmap='jet')
    ax.contourf(X/d, Y/d, f1, levels=[0.5, 1.0], colors='blue',alpha=0.70)
    ax.contourf(X/d, Y/d, f2, levels=[0.5, 1.0], colors='red',alpha=0.70)
    ax.contour(X/d, Y/d, f1, levels=0.5, colors='blue')
    ax.contour(X/d, -Y/d, f1, levels=0.5, colors='blue')
    ax.contour(X/d, Y/d, f2, levels=0.5, colors='red')
    ax.contour(X/d, -Y/d, f2, levels=0.5, colors='red')
    ax.set_xlabel(r'$X/D$', fontsize=30)
    ax.set_ylabel(r'$Y/D$', fontsize=30)
    plt.axis('equal')
    plt.xlim(xmin/d, xmax/d)
    plt.ylim(-ymax/d, ymax/d)
    plt.title('t = %5.4f s' % t, fontsize=30)
    plt.show()
    # plt.savefig(name)
    plt.close()
    print(("Done %d of %d" % (ti+1, nGFS)))
