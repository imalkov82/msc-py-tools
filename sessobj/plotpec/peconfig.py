__author__ = 'imalkov'

import pandas as pnd
import os

# data = {'step0':    [   0,     0,      0,      0,      0,     0,      0,      0,      0,      0,      0,      0,     0,     0,    0],
#         'step1':    [2000,  3000,   3000,      0,   1000,  2000,   3000,   3000,   2000,   3000,   3000,   1500,  5000,  6000,  7000],
#         'step2':    [5000,  6000,   7000,      0,   2000,  5000,   6000,   7000,   5000,   6000,   7000,   3500, 10000, 12000, 14000],
#         'row_num':  [453,   453,    453,     453,    453,   453,    453,    453,    453,    453,    453,    453, 453,     453,   453],
#         'col_num':  [808,   808,    808,     808,    808,   808,    808,    808,    808,    808,    808,    808, 808,     808,   808],
#         'execution_directory': [
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1B/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1C/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1D/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2A/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2B/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2C/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1D/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE03/Session1A/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE03/Session1B/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE03/Session1C/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2D/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2E/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2F/',
#                     '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2G/'
#                     ]
#         }

# topo_data = pnd.read_csv(os.path.join(os.getcwd(),'../../topogen/peconfig.csv'), names = ['execution_directory','col_num','row_num','step0','step1','step2'])
main_dir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/'.format(os.environ['HOME'])
# topo_data = pnd.read_csv('{0}/Dropbox/M.s/Research/DOCS/peconfig.csv'.format(os.environ['HOME']), names = ['execution_directory','col_num','row_num','step0','step1','step2', 'status'])
topo_data = pnd.read_csv('{0}/Dropbox/M.s/Research/DOCS/peconfig.csv'.format(os.environ['HOME']), names = ['execution_directory','col_num','row_num','step0','step1','step2', 'status'])
wrk_data = topo_data[topo_data['status'] == 0]
wrk_data['execution_directory'] = work_data['execution_directory'].apply(lambda x : x.replace('~', os.environ['HOME']))
# wrk_list = [p for i,p in work_data['execution_directory'].iteritems()]

# indxs = [
#     'run',
#     'topofname',
#     'nx0', 'ny0',
#     'dlon', 'dlat',
#     'nskip',
#     'lon0', 'lat0',
#     'nstep',
#     'tau',
#     't_2', 'a_2', 'o_2', 'io_2',
#     't_1', 'a_1', 'o_1', 'io_1',
#     't_0', 'a_0', 'o_0', 'io_0',
#     'f0', 'rc', 'rm', 'E', 'n', 'L', 'nx', 'ny',
#     'zl', 'nz', 'k', 'tb', 'tt', 'la', 'pr',
#     'agefnme',
#     'file_dir']
#
#
# failt_2_2 = [
# 'nfault',
# 'x1','y1','x2','y2',
# 'n_0',
# 'ri_0','si_0',
# 'ri_1','si_1',
# 'nstep_0',
# 'tstart_0','tend_0','velo_0',
# 'nstep_1',
# 'tstart_1','tend_1','velo_1']

# homedir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/'.format(os.environ['HOME'])
#
# df1 = pd.DataFrame()
#
# arr = []
# for el in [os.path.join(homedir,el) for el in sorted(os.listdir(homedir))]:
#     topo_path = os.path.join(el,'input')
#     tll = topo_parser(os.path.join(topo_path,'topo_parameters.txt'))
#     arr.append(tll.split(',') + [el])
#
# for i, nm in enumerate(indxs):
#     df1[nm] = [el[i] for el in arr]
