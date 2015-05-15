__author__ = 'imalkov'

import pandas as pnd
import  matplotlib.pylab as plt
import numpy as np
import os
import session3 as s3



def print_mean(fs, col_name_arr, query_str):
    res = []
    for t in col_name_arr:
        fs = fs.query(query_str)
        res.append(-1 * fs[t].mean())
    return res


def temperature_from_files(root_path, col_name_arr, file_extention = '.csv', on_point_func = lambda x : x):
    res = []
    for i,t in enumerate(col_name_arr):
        tmp_df = pnd.read_csv('{0}/Temperature{1}.{2}'.format(root_path, i, file_extention), usecols = ['arc_length','Points:2'])
        tmp_df[t] = on_point_func(tmp_df['Points:2'])
        tmp_df.drop('Points:2', axis= 1 , inplace= True)
        res.append(tmp_df)
    return reduce(lambda f1, f2: pnd.merge(f1, f2, on='arc_length', how='outer'), res)


def riv_esc_extention(tpath):
    '''
    detect type of csv file
    '''
    if tpath.find('esc') != -1 :
        suf = '_esc'
    elif tpath.find('riv') != -1:
        suf = '_riv'
    else:
        suf = ''
    return suf

def save_ea_to_file(tpath , dst_ext_func = lambda x: ''):

    dst_root = '/home/imalkov/Dropbox/M.s/Research/PICTURES/GEOTHERM/'
    dst_fig_name = '{0}/{1}_geoth{2}.pdf'.format(dst_root,s3.name_dst_file(tpath), dst_ext_func(tpath))

    max_high = max(pnd.read_csv('{0}/Age-Elevation0.csv'.format(tpath), usecols=['Points:2'])['Points:2'])

    print  'file {0} \n max height: {1}'.format(tpath, max_high)

    point_lables = ['{0}C'.format(i * 25) for i in xrange(1,5)]
    fs = temperature_from_files(tpath, point_lables, on_point_func=lambda x: x - max_high)

    f = plt.figure()
    ax = f.gca()
    for i in point_lables:
        ax = fs.plot(x='arc_length', y=i, ax=ax)

    txs = np.linspace(0, -12, 25)
    plt.title('BLOCK GEOTHREMA', fontsize = 12)
    plt.legend(point_lables, loc='best', fontsize=10)
    plt.xlabel('Length [km]')
    plt.ylabel('Depth [Km]')
    plt.yticks(txs, ['0'] + [str(-i) for i in txs[1:]])

    plt.show()
    print  'save figure to: {0}'.format(dst_fig_name)
    # plt.savefig(ff)





