__author__ = 'imalkov'

import pandas as pnd
import  matplotlib.pylab as plt
import numpy as np
import os


def save_to_file(tpath):
    arr = []
    node_loc = tpath.find('NODE') + len('NODE')
    s_loc = tpath.find('csv') - 3
    fig_name = 'n{0}s{1}'.format(tpath[node_loc:node_loc + 2], tpath[s_loc:s_loc + 2])
    f = plt.figure()
    ax = f.gca()

    max_height = max(pnd.read_csv('{0}/Age-Elevation0.csv'.format(tpath), usecols = ['Points:2'])['Points:2'])
    for i in xrange(4):
        tmp_df = pnd.read_csv('{0}/Temperature{1}.csv'.format(tpath, i), usecols = ['arc_length','Points:2'])
        tmp_df['Points_{0}'.format(25 * (i + 1))] =  tmp_df['Points:2'] - max_height
        tmp_df.drop('Points:2', axis= 1 , inplace= True)
        arr.append(tmp_df)


    fs = reduce(lambda f1, f2: pnd.merge(f1, f2, on = 'arc_length', how='outer'), arr)
    # print fs
    # return
    valarr10 = []
    try:
        for i in ['Points_{0}'.format(25 * (i + 1)) for i in xrange(4)]:
            ax = fs.plot(x = 'arc_length' ,y = i)
            # ds = fs[fs['arc_length']  >= 9.5 & fs['arc_length']  <= 10.5][i]
            fs = fs.query('arc_length >= 9.5 and arc_length <= 10.5')
            valarr10.append(-1 * fs[i].mean())
    except Exception,e:
        raise e

    txs = np.linspace(0, -12, 25)
    plt.title('BLOCK GEOTHREMA {0}'.format(['{0}C'.format(i) for i in np.linspace(25,100,4)]), fontsize = 12)
    plt.xlabel('Length [km]')
    plt.ylabel('Depth [Km]')
    # plt.yticks(txs, ['0'] + [str(-i).split('.')[0] for i in txs[1:]])
    plt.yticks(txs, ['0'] + [str(-i) for i in txs[1:]])


    if tpath.find('esc') != -1 :
        suf = '_esc'
    elif tpath.find('riv') != -1:
        suf = '_riv'
    else:
        suf = ''
    ff = '/home/imalkov/Dropbox/M.s/Research/PICTURES/GEOTHERM/{0}_geoth{1}.pdf'.format(fig_name,suf)
    print ff
    print valarr10
    # plt.savefig(ff)



root_path = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/'

for i in sorted([root_path + p + '/csv/' for p in os.listdir(root_path)]):
    # save_to_file(os.path.join(i,'escarpment'))
    # save_to_file(os.path.join(i,'riverbad'))
    save_to_file(i)
