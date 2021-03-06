import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
import math as m
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True


def gettingfield(fieldstr):
    exe = "gfs2oogl2D -p cartgrid.dat -c %s < %s" % (fieldstr, place)
    temp1 = sp.check_output(exe, shell=True)
    temp2 = temp1.decode("utf-8")
    temp3 = temp2.split("\n")
    fieldtemp = []
    Xtemp = []
    Ytemp = []
    for n1 in range(0, len(temp3) - 1):
        temp4 = temp3[n1].split(" ")
        Xtemp.append(float(temp4[0]))
        Ytemp.append(float(temp4[1]))
        fieldtemp.append(float(temp4[3]))
    X = np.asarray(Xtemp)
    Y = np.asarray(Ytemp)
    field = np.asarray(fieldtemp)
    X.resize((ny,nx))
    Y.resize((ny,nx))
    field.resize((ny, nx))
    return X, Y, field


# ----------------------------------------------------------------------------------------------------------------------


nGFS = 7
tmp = np.ones(nGFS)

folder = 'Tracer11-12'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 2*1e-3
Ldomain = 4*d*m.sin(120*m.pi/180)
xmin = Ldomain/2 - d
xmax = Ldomain/2 - 0.01*d
ymin = -Ldomain/2
ymax = Ldomain/2
nx = 125
ny = 501
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
z = 0
gridfile = 'cartgrid.dat'
print('saving the grid')
f = open('cartgrid.dat', 'w+')
for i in range(ny):
 for j in range(nx):
     f.write("%f %f %f\n" % (x[j], y[i], 0))
f.close()
for ti in range(nGFS):
    t = 0.0005 * ti
    name = "%s/%4.4d.png" %(folder, ti)
    plt.figure(figsize=(19.20, 10.80))
    rc('axes', linewidth=2)
    # for case 5
    ax1 = plt.subplot(2,1,1)
    place = "case11/intermediate/sim%5.4f.gfs" % t
    X, Y, f = gettingfield('f')
    Xp, Yp, fp = gettingfield('fp')
    X.transpose()
    Y.transpose()
    f.transpose()
    Xp.transpose()
    Yp.transpose()
    fp.transpose()
    ax1.contour(Y/d, X/d, f, levels=0.5, colors='b')
    ax1.contourf(Yp/d, Xp/d, fp, levels=[0.5, 1], colors='r')
    #ax1.set_xlabel(r'$X/D$', fontsize=30)
    ax1.set_ylabel(r'$Y/D$', fontsize=30)
    plt.axis('square')
    ax1.set_ylim(xmax/d, xmin/d)
    ax1.set_xlim(ymin/d, ymax/d)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.title('t = %5.4f s' % t, fontsize=30)
    # for case 6
    ax2 = plt.subplot(2,1,2)
    place = "case12/intermediate/sim%5.4f.gfs" % t
    X, Y, f = gettingfield('f')
    Xp, Yp, fp = gettingfield('fp')
    X.transpose()
    Y.transpose()
    f.transpose()
    Xp.transpose()
    Yp.transpose()
    fp.transpose()
    ax2.contour(Y/d, X/d, f, levels=0.5, colors='b')
    ax2.contourf(Yp/d, Xp/d, fp, levels=[0.5, 1], colors='r')
    ax2.set_xlabel(r'$X/D$', fontsize=30)
    ax2.set_ylabel(r'$Y/D$', fontsize=30)
    plt.axis('square')
    ax2.set_ylim(xmax/d, xmin/d)
    ax2.set_xlim(ymin/d, ymax/d)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    #plt.show()
    plt.savefig(name)
    plt.close()
    print(("Done %d of %d" % (ti+1, nGFS)))
