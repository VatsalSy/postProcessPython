## this is a simple script to generate .ppm images from gerris simulation files (GFSfile) using the gfs-view GFV file
## GFSfile=intermediate/sim20.0.gfs GFV=T.gfv image=test sh GenerateImages2.sh
## Please this is for 2 dimensional simulations
(for i in `seq 1 1 1`; do
cat $GFSfile
echo "Save $image.ppm { width = 1280 height = 800 }"
done ) | gfsview-batch2D $GFV
