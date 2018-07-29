# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids

import numpy as np
import os
import subprocess as sp

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

folderData = 'OutputData'  # output folder
if not os.path.isdir(folderData):
    os.makedirs(folderData)

d = 2*1e-3
Ldomain = 8*d
# These are based on the GFSview coordinates
xmin = -0.50*Ldomain
xmax = -0.50*Ldomain + d
ymin = -0.25*Ldomain
ymax = 0.25*Ldomain
nx = 500
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
        nameData = "%s/%5.4f.txt" % (folderData, t)
        # Transformation from GFS coordinate system to Basilisk coordinate system
        xp = -y/d
        yp = (x - xmin)/d
        Xp = -Y.transpose()/d
        Yp = (X.transpose() - xmin)/d
        Up = -V.transpose()
        Vp = U.transpose()
        f1p = f1.transpose()
        f2p = f2.transpose()
        # From here: Notice the changes for the file fieldTxtplot.py
        f = open(nameData, "w")
        f.write("x y f1 f2 U V\n")
        nxp = ny
        nyp = nx
        for i in range(nyp):
            for j in range(nxp):
                f.write("%f %f %f %f %f %f\n" % (Xp[i,j], Yp[i,j], f1p[i,j], f2p[i,j], Up[i,j], Vp[i,j]))
        f.close()
        print(("Done %d of %d" % (ti+1, nGFS)))
