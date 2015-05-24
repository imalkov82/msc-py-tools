__author__ = 'imalkov'
import numpy as np
import os
from argparse import ArgumentParser
import pandas as pnd
import shutil
import datetime

#########################################################
def gen_mgsurf(xsize,ysize,foo):
    x  = np.linspace(0, xsize, xsize)
    y  = np.linspace(0, ysize ,ysize)
    xi,yi = np.meshgrid(x,y)
    return foo(xi,yi)

def write_topo_fname(data, ptxt):
    try:
        np.savetxt(ptxt, data.flatten(),fmt='%d')
    except Exception, e:
        print "Error in Print" + str(e)

###########################################################
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
        zl = gen_mgsurf(cynlocation, fylocation, lambda xi,yi: 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0)) * yi)
        z = np.concatenate((np.fliplr(zl),zl),axis=1)
        z = np.hstack((z,np.zeros((z.shape[0],1))+fw_max)) #add column
        #escarpment
        st2 = gen_mgsurf(mrow,fylocation,lambda xi,yi: 101 * np.tan(np.deg2rad(60)) * yi)
        #final topography
        st2[z<st2] = z[z<st2]
        st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)
        st2[st2 > fw_max] = fw_max # footwall maximum height (4 km = 4000 m)
        return st2
    return surfcyn_gen

######################################################################################################
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

###########################################################
def main(bin_loc, genv_flag, cyn_flag, disp_path):

    # main_dir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/'.format(os.environ['HOME'])
    topo_data = pnd.read_csv('{0}/Dropbox/M.s/Research/DOCS/peconfig.csv'.format(os.environ['HOME']), names = ['execution_directory','col_num','row_num','step0','step1','step2', 'env', 'test', 'pecube'])
    wrk_data = topo_data[topo_data['env'] == 0]
    wrk_data['execution_directory'] = wrk_data['execution_directory'].apply(lambda x : x.replace('~', os.environ['HOME']))

    # col, _ = wrk_data.shape

    # for i in xrange(col):
    for ind, s in wrk_data.iterrows():
        #cteate environment
        # s = wrk_data.ix[i]
        rootpath = s['execution_directory'].replace('~', os.environ['HOME'])
        print  'execute path = {0}'.format(rootpath)
        if disp_path is True:
            continue

        if os.path.isdir(rootpath) is False:
            print 'create dir:{0}'.format(rootpath)
            os.mkdir(rootpath)
        if genv_flag is True:
            print 'create environment:{0}'.format(rootpath)
            gen_env(rootpath,binpath = bin_loc)
        # gen_env(rootpath,binpath = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/bin/')

        if cyn_flag is True:
            print 'generate topography with canyon'
            zs_func = surfcyn_gen_factory(s['row_num'],s['col_num'])
        else:
            print 'generate topography'
            zs_func = surfgen_factory(s['row_num'],s['col_num'])
        dir_surfs = [zs_func(s['step{0}'.format(j)] * np.sin(np.deg2rad(60)), gen_mgsurf) for j in xrange(3)]

        data_path = os.path.join(rootpath, 'data')
        print 'write topography to file'
        for k, zs in enumerate(dir_surfs):
            write_topo_fname(zs,os.path.join(data_path,'step{0}.txt'.format(k)))
#######################################################################################
if __name__ == '__main__':
    parser = ArgumentParser()
    #set rules
    parser.add_argument( "-l", dest="bin_location", help="source directory", default= '')
    parser.add_argument( "-g", action="store_true", dest="gen_env", help="generate environment flag", default=False)
    parser.add_argument( "-c", action="store_true", dest="cyn_flag", help="generate 3D geomery (default is 2D)", default=False)
    parser.add_argument( "-p", action="store_true", dest="disp_path", help="display path", default=False)
    kvargs = parser.parse_args()

    main(kvargs.bin_location, kvargs.gen_env, kvargs.cyn_flag, kvargs.disp_path)