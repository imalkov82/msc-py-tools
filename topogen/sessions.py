#resolution of 101 m = 0.00067 angle
#------------------------------------
#grid size
from PECUBE_RUN import *
import numpy as np
from pec_config import topo_data
import os
import shutil
import datetime

def surf_generator(mrow, mcol):
    fylocation = mcol/2
    def foo(fw_maxh, f):
        st2 = f(mrow,fylocation,lambda xi,yi: 101 * np.tan(np.deg2rad(60)) * yi)
        st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)
        st2[st2 > fw_maxh] = fw_maxh # footwall maximum height
        return st2
    return foo


col,row = topo_data.shape

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

def gen_env(rootpath, binpath):
    try:
        create_bindir(rootpath, binpath)
        create_inputdir(rootpath)
        create_outdir(rootpath)
        create_datadir(rootpath)
        create_vtkdir(rootpath)
    except Exception, e:
        print "fail to create dir: msg {0}".format(e.message)


for i in xrange(3, row):
    #cteate environment
    s = topo_data.ix[i]
    rootpath = s['execution_directory'].replace('~', os.environ['HOME'])
    print  'execute path = {0}'.format(rootpath)
    if os.path.isdir(rootpath) is False:
        os.mkdir(rootpath)

    # gen_env(rootpath,'')

    s = topo_data.ix[i]
    zs_func = surf_generator(s['row_num'],s['col_num'])
    dir_surfs = [zs_func(s['step{0}'.format(j)] * np.sin(np.deg2rad(60)), genMGSurfe) for j in xrange(3)]
    data_path = os.path.join(rootpath, 'data')
    for k, zs in enumerate(dir_surfs):
        writeToTopofname(zs,os.path.join(data_path,'step{0}.txt'.format(k)))
