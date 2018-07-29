# postProcessPython
This is a collection of post processing modules for Gerris and Basilisk C

fieldGFS:
fieldExtraction_v1.py
This is a verbatim transformation of MATLAB post-processing code to python. The earlier version can be found here: https://github.com/VatsalSy/FluidChians/tree/master/PostProcessing

fieldExtraction_v2.py
The only (major) difference comes in the removal of meshgrid function. Instead, the function "gettingfield" also returns the values of X and Y. The initial mesh is formed by using linear x and y vectors. 

Drop Spitting:
OneGraph.py
Similar to fieldExtraction but here, I plot two different simulation contours together to compare (at a given time)
