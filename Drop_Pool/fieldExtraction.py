import numpy as np
import os
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True


def gettingfield(fieldstr,gridfile):
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

folder = 'Tracer'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

d = 2*1e-3
Th = 0.001
Thi = 1-Th
Ldomain = 4*d
xmin = -0.25*Ldomain
xmax = 0.25*Ldomain
ymin = 0.0*Ldomain
ymax = 0.5*Ldomain
nx = 751
ny = 1001
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
z = 0
print('saving the grid')
gridfileT = 'cartgridT.dat'
fg = open(gridfileT, 'w+')
for i in range(ny):
 for j in range(nx):
     fg.write("%f %f %f\n" % (x[j], y[i], 0))
fg.close()
X, Y = np.meshgrid(x,y,indexing='xy')
print('saved the grid')
for ti in range(nGFS):
    t = 0.0005 * ti
    place = "intermediate/sim%5.4f.gfs" % t
    if not os.path.exists(place):
        print("File not found!")
    else:
        f1 = gettingfield('f1',gridfileT)
        f2 = gettingfield('f2',gridfileT)
        name = "%s/%4.4d.png" %(folder, ti)
        fig, ax = plt.subplots()
        fig.set_size_inches(19.20, 10.80)
        rc('axes', linewidth=2)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        ax.contourf(Y.transpose()/d, X.transpose()/d, f1.transpose(), levels=[0.5, 1.0], colors='b',alpha=0.70)
        ax.contourf(-Y.transpose()/d, X.transpose()/d, f1.transpose(), levels=[0.5, 1.0], colors='b',alpha=0.70)
        ax.contourf(Y.transpose()/d, X.transpose()/d, f2.transpose(), levels=[0.5, 1.0], colors='r',alpha=0.70)
        ax.contourf(-Y.transpose()/d, X.transpose()/d, f2.transpose(), levels=[0.5, 1.0], colors='r',alpha=0.70)
        ax.set_xlabel(r'$Y/D$', fontsize=30)
        ax.set_ylabel(r'$X/D$', fontsize=30)
        plt.axis('square')
        plt.ylim(xmax/d, xmin/d)
        plt.xlim(-ymax/d, ymax/d)
        plt.title(r't = %5.4f s' % t, fontsize=30)
        #plt.show()
        plt.savefig(name)
        plt.close()
        print(("Done %d of %d" % (ti+1, nGFS)))
