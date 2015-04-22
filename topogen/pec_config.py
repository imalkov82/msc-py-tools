__author__ = 'imalkov'

import pandas as pd
from inputgroup.toporule import topo_parser
import os

data = {'step0':    [0,     0,      0,      0,      0,      0],
        'step1':    [2000,  3000,   3000,   0,   1000,   1500],
        'step2':    [5000,  6000,   7000,   0,   2000,   3500],
        'row_num':  [453,   453,    453,    453,    453,    453],
        'col_num':  [808,   808,    808,    808,    808,    808],
        'execution_directory': [
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/',
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1B/',
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1C/',
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1D/',
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1E/',
                    '~/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1F/']
        }

topo_data = pd.DataFrame(data)

indxs = [
    'run',
    'topofname',
    'nx0', 'ny0',
    'dlon', 'dlat',
    'nskip',
    'lon0', 'lat0',
    'nstep',
    'tau',
    't_2', 'a_2', 'o_2', 'io_2',
    't_1', 'a_1', 'o_1', 'io_1',
    't_0', 'a_0', 'o_0', 'io_0',
    'f0', 'rc', 'rm', 'E', 'n', 'L', 'nx', 'ny',
    'zl', 'nz', 'k', 'tb', 'tt', 'la', 'pr',
    'agefnme',
    'file_dir']

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
