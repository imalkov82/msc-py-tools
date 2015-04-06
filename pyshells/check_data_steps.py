__author__ = 'imalkov'

import os
import numpy

for root, dirs, files in os.walk('/home/imalkov/Dropbox/M.s/Research/DATA/BDTOPO/TOPO_TYPE13', followlinks=True):
    if 'step0.txt' in files:
        s = root + '\n'
        files.sort()
        max_val = 0
        first = True
        for file in files:
            arr = numpy.loadtxt(os.path.join(root,file))
            if first and arr.max() != 0:
                s = ''
                break
            else:
                first = False
            if max_val <= arr.max():
                s += file + ' ' + str(arr.min()) + ' ' + str(arr.max()) + '\n'
                max_val = arr.max()
            else:
                s = ''
                break
        print(s)

