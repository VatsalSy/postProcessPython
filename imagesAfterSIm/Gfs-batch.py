import numpy as np
import os

nGFS = 41
tmp = np.ones(nGFS)

GFVfile = 'Tshow.gfv'
folder = 'Video2'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

for i in range(nGFS):
    t = 0.0005 * i
    place = "intermediate/sim%5.4f.gfs" % t
    if not os.path.exists(place):
        print("File not found!")
    else:
        os.system("GFSfile=%s GFV=%s image=%s/Figure%4.4d.ppm sh GenerateImages2.sh" % (place, GFVfile, folder, i))
        print("%d of %d" %(i, nGFS))
