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


def gettingfield(fieldstr):
    print('Getting %s' % fieldstr)
    exe = "gfs2oogl2D -p %s -c %s < %s" % (gridfile,fieldstr, place)
    temp1 = sp.check_output(exe, shell=True)
    temp2 = temp1.decode("utf-8")
    temp3 = temp2.split("\n")
    fieldtemp = []
    for n1 in range(0, len(temp3) - 1):
        temp4 = temp3[n1].split(" ")
        fieldtemp.append(float(temp4[3]))
    field = np.asarray(fieldtemp)
    field.resize((ny, nx))
    print('Completed %s' % fieldstr)
    return field

# ----------------------------------------------------------------------------------------------------------------------


nGFS = 1
tmp = np.ones(nGFS)

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 2*1e-3
Ldomain = 8*d
# These are based on the GFSview coordinates
xmin = -0.50*Ldomain
xmax = -0.50*Ldomain + d
ymin = -0.25*Ldomain
ymax = 0.25*Ldomain
nx = 500
ny = 1000
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
z = 0
print('saving the grid')
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
gridfile = 'cartgrid.dat'
fg = open(gridfile, 'w+')
for i in range(ny):
 for j in range(nx):
     fg.write("%f %f %f\n" % (x[j], y[i], 0))
fg.close()
X, Y = np.meshgrid(x,y,indexing='xy')
print('saved the grid')
# GFSview coordinates end!
for ti in range(nGFS):
    t = 0.0005 * 4
    place = "intermediate/snapshot-%5.4f.gfs" % t
    if not os.path.exists(place):
        print("File not found!")
    else:
        f1 = gettingfield('f1')
        f2 = gettingfield('f2')
        U = gettingfield('U')
        V = gettingfield('V')
        name = "%s/%4.4d.png" % (folder, ti)
        fig, ax = plt.subplots()
        fig.set_size_inches(19.20, 10.80)
        rc('axes', linewidth=2)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        # Transformation from GFS coordinate system to Basilisk coordinate system
        xp = -y/d
        yp = (x - xmin)/d
        Xp = -Y.transpose()/d
        Yp = (X.transpose() - xmin)/d
        Up = -V.transpose()
        Vp = U.transpose()
        f1p = f1.transpose()
        f2p = f2.transpose()
        # Uncomment if you want to see it as GFSview system
        # yp = y/d
        # xp = (x - xmin)/d
        # Yp = Y/d
        # Xp = (X - xmin)/d
        # Vp = V
        # Up = U
        speed = np.sqrt(Up**2 + Vp**2)
        maxs = speed.max()
        if maxs > 0:
            Up /= maxs
            Vp /= maxs
            speed /= maxs
        ax.streamplot(xp, -yp, Up, -Vp, density = 6, color = speed, linewidth=1, cmap='Greys')
        ax.contourf(Xp, Yp, f1p, levels=[0.5, 1.0], colors='blue',alpha=0.70)
        ax.contourf(Xp, Yp, f2p, levels=[0.5, 1.0], colors='red',alpha=0.70)
        ax.contour(Xp, Yp, f1p, levels=0.5, colors='blue')
        ax.contour(Xp, Yp, f2p, levels=0.5, colors='red')
        ax.contour(Xp, -Yp, f1p, levels=0.5, colors='blue')
        ax.contour(Xp, -Yp, f2p, levels=0.5, colors='red')
        ax.set_xlabel(r'$X/D$', fontsize=30)
        ax.set_ylabel(r'$Y/D$', fontsize=30)
        plt.axis('equal')
        plt.xlim(xp.min(), xp.max())
        plt.ylim(-yp.max(), yp.max())
        plt.title('t = %5.4f s' % t, fontsize=30)
        # plt.show()
        plt.savefig(name)
        plt.close()
        print(("Done %d of %d" % (ti+1, nGFS)))
