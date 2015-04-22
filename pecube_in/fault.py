__author__ = 'imalkov'

import numpy
from inputgroup.toporule import topo_parser
import pandas
from pandas import Series, DataFrame

class Fault:
    def __init__(self, n, nstep, x , y, x1, x2, y1, y2, timestart, timeend, velo, xs, ys, xn, yn):
        self.n  = n
        self.nstep = nstep
        self.x = x
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.timestart = timestart
        self.timeend = timeend
        self.velo = velo
        self.xs = xs
        self.ys = ys
        self.xn = xn
        self.yn = yn



# def create_pecube_in(faults, nd, locrange, param):
def create_pecube_in(faults, nd, locrange, param, mpath):
    print topo_parser(mpath)

def calculate_fault_parameters(faults):
    for fault in faults:
        for k in range(fault.n - 1):
            xn = fault.x[k-1] - fault.x[k]
            yn = fault.y[k-1] - fault.y[k]
            xyn = numpy.sqrt(xn**2 + yn**2)
            xn = xn/xyn
            yn = yn/xyn
            fault.xs[k] = xn
            fault.ys[k] = yn
    return faults

# param = numpy.ones(1024)
# locrange = numpy.ones((2,1024))
# misfit = 0.0
# nd = nfault = nproc = iproc = ierr = 0
# iq = 'c'

mpath = '/home/imalkov/Documents/Future_Documents/GDRIVE_POST/Research/Projects/FPM/BGUPec/input/topo_parameters.txt'
topoprms = topo_parser(mpath).split(',')
pivot = 9
split_p0 = pivot + 1
split_p1 = pivot + 2
split_p2 = split_p1 + 4 * (int(topoprms[pivot]) + 1)
split_p3 = split_p2 + 1
split_p4 = split_p3 + 7

# print topoprms
s1 =  Series(topoprms[:pivot], index=['run', 'fnme', 'nx0', 'ny0', 'dx', 'dy', 'nskip', 'xlon', 'xlat'])
s2 =  Series([topoprms[split_p0]],index=['tau'])
sll = topoprms[split_p1:split_p2]
# [sll[4*i: 4 * (i + 1)] for i in xrange(int(topoprms[pivot]) + 1)]

data = {'timek': [], 'topomag': [], 'topooffset': [], 'iout':[]}
timek = []
topomag = []
topooffset = []
iout = []

for i in xrange(int(topoprms[pivot]) + 1):
    timek.append(sll[4*i])
    topomag.append(sll[4*i + 1])
    topooffset.append(sll[4*i + 2])
    iout.append(sll[4*i + 3])

data = {'timek':timek,'topomag':topomag,'topooffset':topooffset,'iout':iout}

df1 = DataFrame(data, columns = ['timek','topomag','topooffset','iout'] ,index= [str(i) + ')' for i in range(1,4)])
s3 = Series(topoprms[split_p2:split_p3], index= ['isoflag'])
s4 = Series(topoprms[split_p3:split_p4], index= ['rhoc', 'rhom', 'young', 'poisson', 'thickness', 'nxiso', 'nyiso'])
s5 = Series(topoprms[split_p4:-1], index=['crustal_thickness', 'nz', 'diffusivity', 'tmax', 'tmsl', 'tlapse', 'heatproduction'])
s6 = Series([topoprms[-1]], index=['obsfile'])

s16 = pandas.concat([s1,s2, s3, s4, s5, s6])
print s16
print df1