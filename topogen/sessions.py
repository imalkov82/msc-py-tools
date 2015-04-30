#resolution of 101 m = 0.00067 angle
#------------------------------------
#grid size
from PECUBE_RUN import *
import numpy as np
from pec_config import topo_data
import os
import shutil
import datetime
import pandas as pnd
import  matplotlib.pylab as plt
import numpy

def surfgen_factory(mrow, mcol):
    fylocation = mcol/2
    def surf_generator(fw_maxh, f):
        st2 = f(mrow,fylocation,lambda xi,yi: 101 * np.tan(np.deg2rad(60)) * yi)
        st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)
        st2[st2 > fw_maxh] = fw_maxh # footwall maximum height
        return st2
    return surf_generator

def surfcyn_gen_factory(mrow, mcol):
    fylocation = mcol/2
    cynlocation = mrow / 2 # canyon location
    def surfcyn_gen(fw_max, f):
        zl = genMGSurfe(cynlocation, fylocation, lambda xi,yi: 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0)) * yi)
        z = np.concatenate((np.fliplr(zl),zl),axis=1)
        z = np.hstack((z,np.zeros((z.shape[0],1))+fw_max)) #add column
        #escarpment
        st2 = genMGSurfe(mrow,fylocation,lambda xi,yi: 101 * np.tan(np.deg2rad(60)) * yi)
        #final topography
        st2[z<st2] = z[z<st2]
        st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)
        st2[st2 > fw_max] = fw_max # footwall maximum height (4 km = 4000 m)
        return st2
    return surfcyn_gen

def create_bindir(path, symlinkdir):
    bin_path = os.path.join(path,'bin')
    os.mkdir(bin_path)
    for p in ['Vtk', 'Pecube', 'Test']:
        os.popen('ln -n {0} {1}'.format(os.path.join(symlinkdir,p),os.path.join(bin_path,p)))

def create_inputdir(path, topo_params_list = [], fault_params_list = []):
    indir = os.mkdir(os.path.join(path, 'input'))
    if len(topo_params_list) > 0:
        with open(os.path.join(indir,'topo_params.txt'), 'w') as f:
            pass

    if len(fault_params_list) > 0:
        with open(os.path.join(indir,'topo_params.txt'), 'w') as f:
            pass

def create_outdir(path):
    os.mkdir(os.path.join(path,'peout'))

def create_datadir(path, steps_list = []):
    data_dir = os.path.join(path,'data')
    os.mkdir(data_dir)
    for step in steps_list:
        shutil.copy2(step, data_dir)

def create_vtkdir(path):
    vtk_path = os.path.join(path,'VTK')
    if os.path.isdir(vtk_path):
        os.popen('mv {0} {1}'.format(vtk_path, 'VTK_'+ (datetime.datetime.now().isoformat()).replace(':','_')))
    os.mkdir(vtk_path)


def read_plot_trend_csv(fpath):
    df1 = pnd.read_csv(fpath)
    b = df1[(df1['Points:2'] > min(df1['Points:2'])) & (df1['Points:2'] < max(df1['Points:2'])) ]
    b.plot(x='ApatiteHeAge', y='Points:2', style='o-r')
    # calc the trendline (it is simply a linear fitting)
    z = numpy.polyfit(b['ApatiteHeAge'],b['Points:2'], 1)
    p = numpy.poly1d(z)
    # the line equation:
    print 'y=%.6fx+(%.6f)'%(z[0],z[1])

def gen_env(rootpath, binpath):
    try:
        create_bindir(rootpath, binpath)
        create_inputdir(rootpath)
        create_outdir(rootpath)
        create_datadir(rootpath)
        create_vtkdir(rootpath)
    except Exception, e:
        print "fail to create dir: msg {0}".format(e.message)


#--------------- topo generation -----------------------------------
# col, _ = topo_data.shape
#
#
# for i in xrange(9, col):
#     #cteate environment
#     s = topo_data.ix[i]
#     rootpath = s['execution_directory'].replace('~', os.environ['HOME'])
#     print  'execute path = {0}'.format(rootpath)
#     if os.path.isdir(rootpath) is False:
#         os.mkdir(rootpath)
#
#     gen_env(rootpath,binpath = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/bin/')
#
#     s = topo_data.ix[i]
#     zs_func = surfcyn_gen_factory(s['row_num'],s['col_num'])
#     # zs_func = surfgen_factory(s['row_num'],s['col_num'])
#     dir_surfs = [zs_func(s['step{0}'.format(j)] * np.sin(np.deg2rad(60)), genMGSurfe) for j in xrange(3)]
#     data_path = os.path.join(rootpath, 'data')
#     for k, zs in enumerate(dir_surfs):
#         writeToTopofname(zs,os.path.join(data_path,'step{0}.txt'.format(k)))
# --------------------------- SEND BOX ---------------------------------------------------------------------


frame1 = pnd.read_csv('/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1C/csv/Age-Elevation.csv', usecols = ['ApatiteHeAge','Points:2'])

fd = frame1[(frame1['Points:2'] < max(frame1['Points:2']))
             & (frame1['Points:2'] > min(frame1['Points:2']))]

fd['Elevation'] = fd['Points:2'] - min(frame1['Points:2'])

sup_age = 45
x = fd[fd['ApatiteHeAge'] < sup_age]['ApatiteHeAge']
y = fd[fd['ApatiteHeAge'] < sup_age]['Points:2']
z = numpy.polyfit(x,y, 1)
p = numpy.poly1d(z)
print 'y=%.6fx+(%.6f)'%(z[0],z[1])
# plt.plot(x * z[0], z[1])

#TODO: append treadline to plot
f = plt.figure()
ax = fd.plot(x = 'ApatiteHeAge', y = 'Elevation', style = '-o', ax = f.gca())
plt.title('Age-Elevation')
plt.xlabel('ApatiteHeAge [Ma]')
plt.ylabel('Elevation [Km]')

n = numpy.linspace(32,50,10)
plt.plot(n,p(n)- min(frame1['Points:2']),'-r')

plt.show()

