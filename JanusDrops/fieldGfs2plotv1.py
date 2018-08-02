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
    return field

# ----------------------------------------------------------------------------------------------------------------------


nGFS = 81
tmp = np.ones(nGFS)

folder = 'Tracer2'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 2*1e-3
Ldomain = 8*d
# These are based on the GFSview coordinates
xmin = -0.50*Ldomain
xmax = -0.50*Ldomain + d
ymin = -0.5*Ldomain
ymax = 0.5*Ldomain
nx = 750
ny = 1000
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
# GFSview coordinates end!
for ti in range(nGFS):
    t = 0.0005 * ti
    place = "intermediate/snapshot-%5.4f.gfs" % t
    if not os.path.exists(place):
        print("File not found!")
    else:
        f1 = gettingfield('f1')
        # Making refrence at the first droplet (f1): Note that X for Basilisk is Y of GFSview
        sumx = 0.0
        weight = 0.0
        for row in range(len(Y)):
            for col in range(len(Y[0])):
                if f1[row,col] > 0:
                    weight += f1[row,col]
                    sumx += Y[row,col]*f1[row,col]
        sumx /= weight
        ## Part to plot
        # These are based on the GFSview coordinates
        if ((sumx - 1.75*d) < -0.5*Ldomain):
            ymin = -0.5*Ldomain
        else: ymin = sumx - 1.75*d
        if ((sumx + 1.25*d) > 0.5*Ldomain):
            ymax = 0.5*Ldomain
        else: ymax = sumx + 1.25*d
        print('saving the grid for plotting')
        y = np.linspace(ymin, ymax, num=ny)
        gridfile = 'cartgrid.dat'
        fg = open(gridfile, 'w+')
        for i in range(ny):
         for j in range(nx):
             fg.write("%f %f %f\n" % (x[j], y[i], 0))
        fg.close()
        X, Y = np.meshgrid(x,y,indexing='xy')
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
        ## Transformation from GFS coordinate system to Basilisk coordinate system
        xp = -y/d
        yp = (x - xmin)/d
        Xp = -Y.transpose()/d
        Yp = (X.transpose() - xmin)/d
        Up = -V.transpose()
        Vp = U.transpose()
        f1p = f1.transpose()
        f2p = f2.transpose()
        ## Uncomment if you want to see it as GFSview system
        # yp = y/d
        # xp = (x - xmin)/d
        # Yp = Y/d
        # Xp = (X - xmin)/d
        # Vp = V
        # Up = U
        # f1p = f1;
        # f2p = f2;
        ux = 0.0
        weight = 0.0
        for row in range(len(Xp)):
            for col in range(len(Xp[0])):
                if f1p[row,col] > 0:
                    weight += f1p[row,col]
                    ux += Up[row,col]*f1p[row,col]
        ux /= weight
        # Transformation of velocities
        Up += (-ux)
        Xp += (sumx/d)
        xp += (sumx/d)
        speed = np.sqrt(Up**2 + Vp**2)
        maxs = speed.max()
        if maxs > 0:
            ax.streamplot(xp, -yp, Up, -Vp, density = 6, color = speed, linewidth=1, cmap='Greys')
        ax.contourf(Xp, Yp, f1p, levels=[0.5, 1.0], colors='blue',alpha=0.70)
        ax.contourf(Xp, Yp, f2p, levels=[0.5, 1.0], colors='red',alpha=0.70)
        ax.contour(Xp, Yp, f1p, levels=0.5, colors='blue')
        ax.contour(Xp, Yp, f2p, levels=0.5, colors='red')
        ax.contour(Xp, -Yp, f1p, levels=0.5, colors='blue')
        ax.contour(Xp, -Yp, f2p, levels=0.5, colors='red')
        ax.set_xlabel(r'$X/D$', fontsize=30)
        ax.set_ylabel(r'$Y/D$', fontsize=30)
        plt.axis('square')
        plt.xlim(-1.25, 1.75)
        plt.ylim(-yp.max(), yp.max())
        plt.title('t = %5.4f s' % t, fontsize=30)
        #plt.show()
        plt.savefig(name)
        plt.close()
        print(("Done %d of %d" % (ti+1, nGFS)))
