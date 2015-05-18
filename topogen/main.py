__author__ = 'imalkov'

import matplotlib.pylab as plt
import os
import session3 as s3
import sessions2 as s2
import pandas as pnd
from peconfig import topo_data

case01 = False
case02 = False
case03 = False

if case01 is True:
    txs = []
    lebs = []
    save_dir = '/home/imalkov/Dropbox/M.s/Research/PICTURES/AGE-ELEVATION'
    flist = ['/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2A/csv/Age-Elevation0.csv',
             '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/csv/Age-Elevation0.csv']

    f = plt.figure()
    ax = f.gca()

    for f in flist:
        ax =  s3.plot_age_elevation(f, ax)

    print txs
    plt.title('Age-Elevation')
    plt.xlabel('ApatiteHeAge [Ma]')
    plt.ylabel('Elevation [Km]')
    plt.legend(['U=0.2 mm/y, Ex=0','U=0.1 mm/y, Ex=0'], loc='best' , fontsize=10)
    plt.yticks(txs, lebs)
    plt.savefig('{0}/{1}_ae.png'.format(save_dir, '_'.join([s3.name_dst_file(n) for n in flist])))

if case02 is True:
    root_path = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE03/'
    for i in sorted([root_path + p + '/csv/' for p in os.listdir(root_path)]):
        # save_to_file(os.path.join(i,'escarpment'))
        s2.save_ea_to_file(os.path.join(i,'riverbad'))

if case03 is True:
   root_path = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/'
   s2.save_ea_to_file(root_path)

# print
# topo_data.to_csv(os.path.join(os.getcwd(),'peconfig.csv'), index=False, header= False)