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
    exe = "gfs2oogl2D -p cartgrid.dat -c %s < %s" % (fieldstr, place)
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


nGFS = 41
tmp = np.ones(nGFS)

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 2*1e-3
Ldomain = 4*d
xmin = -0.55*Ldomain
xmax = 0.30*Ldomain
ymin = 0.0000*Ldomain
ymax = 0.2*Ldomain
nx = 1000
ny = 500
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
z = 0
gridfile = 'cartgrid.dat'
print('saving the grid')
X, Y = np.meshgrid(x, y, indexing='xy')
f = open('cartgrid.dat', 'w+')
for i in range(ny):
    for j in range(nx):
        f.write("%f %f %f\n" % (X[i, j], Y[i, j], 0))
f.close()
for i in range(nGFS):
    t = 0.0005 * i
    place = "/home/vatsal/research/InAir/MarangoniVsNoM/Case3/Cartesius-Case3-Marangoni/intermediate/sim%5.4f.gfs" % t
    if not os.path.exists(place):
        print("File not found!")
    else:
        T1 = gettingfield('Tpassive1')
        T2 = gettingfield('Tpassive2')
        name = "%s/%4.4d.png" %(folder, i)
        plt.figure(figsize=(19.20, 10.80))
        rc('axes', linewidth=2)
        plt.contourf(X/d, Y/d, T1, levels=[0.5, 1], colors='b')
        plt.contour(X/d, Y/d, T1, levels=[0.5], colors='b')
        plt.contourf(X/d, -Y/d, T1, levels=[0.5, 1], colors='b')
        plt.contour(X/d, -Y/d, T1, levels=[0.5], colors='b')
        plt.contourf(X/d, Y/d, T2, levels=[0.5, 1], colors='r')
        plt.contour(X/d, Y/d, T2, levels=[0.5], colors='r')
        plt.contourf(X/d, -Y/d, T2, levels=[0.5, 1], colors='r')
        plt.contour(X/d, -Y/d, T2, levels=[0.5], colors='r')
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.xlabel(r'$X/D$', fontsize=30)
        plt.ylabel(r'$Y/D$', fontsize=30)
        plt.xlim(xmin, xmax)
        plt.ylim(-ymax, ymax)
        plt.axis('equal')
        # plt.show()
        plt.savefig(name)
        plt.close()
        print(("Done %d of %d" % (i+1, nGFS)))
