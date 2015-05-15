__author__ = 'imalkov'

import pandas as pnd
import os
import numpy as np
import matplotlib.pylab as plt
from argparse import ArgumentParser


def df_ea_riv(frame1):
    fd1 = frame1[frame1['Points:2'] < max(frame1['Points:2'])]
    fd  = fd1[fd1['ApatiteHeAge'] >= 1]
    s = fd[fd['Points:2'] == min(fd['Points:2'])]['arc_length']
    res_df = fd[fd['arc_length'] >= s[s.index[0]]]
    res_df['Elevation'] = res_df['Points:2'] - min(frame1['Points:2'])
    return res_df

def df_ea_esc(frame1):
    fd1 = frame1[(frame1['Points:2'] < max(frame1['Points:2']))
                 & (frame1['Points:2'] > min(frame1['Points:2']))]
    fd  = fd1[fd1['ApatiteHeAge'] >= 1]
    fd['Elevation'] = fd['Points:2'] - min(frame1['Points:2'])
    return fd

def ea_finder(root_dir):
    arr = []
    name = 'Age-Elevation0.csv'
    for dirpath, dirname, filename in os.walk(root_dir):
        if name in filename:
            arr.append(os.path.join(dirpath, name))
    return arr


def collect_to_dict(tup_arr):
    loc_dict = {}
    for el, path in tup_arr:
        arr = []
        if el in loc_dict:
            arr = loc_dict[el]
        arr.append(path)
        loc_dict[el] = arr
    return loc_dict

def temperature_finder(root_dir):
    arr = []
    name = 'Temperature'
    for dirpath, dirname, filename in os.walk(root_dir):
        for f in filename:
            if f.find(name) != -1:
                arr.append((dirpath, f))
    return collect_to_dict(arr)
    # res = []
    # for k , v in collect_to_dict(arr).items():
    #     res += [os.path.join(k,t) for t in v]
    # return res

def name_dst_file(fname, dst_path, suf):
    node_loc = fname.find('NODE') + len('NODE')
    s_loc = fname.find('csv') - 3
    pref = 'n{0}s{1}'.format(fname[node_loc:node_loc + 2], fname[s_loc:s_loc + 2])
    return '{0}{1}'.format(os.path.join(dst_path,pref), suf)

# def get_yticks(min, max):
#     txs = np.linspace(np.round(min), np.ceil(max), 11)
#     lebs = ['0'] + [str(i) for i in txs[1:]]
#     lebs.reverse()
#     return txs, lebs

def plot_ea(frame1, filt_df, dst_path, uplift_rate):
    f = plt.figure()
    ax = filt_df.plot(x='ApatiteHeAge', y='Elevation', style='o-', ax=f.gca())

    plt.title('Age-Elevation')
    plt.xlabel('ApatiteHeAge [Ma]')
    plt.ylabel('Elevation [Km]')

    #tread line
    sup_age = find_max_treadline(filt_df, uplift_rate * np.sin(np.deg2rad(60)))
    x = filt_df[filt_df['ApatiteHeAge'] < sup_age]['ApatiteHeAge']
    y = filt_df[filt_df['ApatiteHeAge'] < sup_age]['Points:2']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    # plt.legend(point_lables, loc='best', fontsize=10)
    # n = np.linspace(min(frame1[frame1['Points:2'] > min(frame1['Points:2'])]['ApatiteHeAge']), max(frame1['ApatiteHeAge']), 21)
    n = np.linspace(min(filt_df[filt_df['Points:2'] >= min(filt_df['Points:2'])]['ApatiteHeAge']), max(filt_df['ApatiteHeAge']), 21)
    plt.plot(n, p(n) - min(frame1['Points:2']),'-r')
    ax.text(np.mean(n), np.mean(p(n) - min(frame1['Points:2'])), 'y=%.6fx + b'%(z[0]), fontsize = 20)


    txs = np.linspace(np.round(min(filt_df['Elevation'])), np.ceil(max(filt_df['Elevation'])), 11)
    lebs = ['0'] + [str(i) for i in txs[1:]]
    plt.yticks(txs, list(reversed(lebs)))
    plt.savefig(dst_path)


def find_max_treadline(data_frame, opt_tread):
    pnd_ds = data_frame['ApatiteHeAge']
    ds = np.array(pnd_ds)
    max_age = 0
    min_tol = 1
    for sup_age in sorted(ds)[1:]:
        # if sup_age >= max_sup_age:
        #     break
        x = data_frame[data_frame['ApatiteHeAge'] < sup_age]['ApatiteHeAge']
        y = data_frame[data_frame['ApatiteHeAge'] < sup_age]['Points:2']
        z = np.polyfit(x, y, 1)
        if abs(opt_tread - z[0]) < min_tol:
            min_tol = abs(opt_tread - z[0])
            max_age = sup_age
    return max_age

def uplift_from_fime_name(fname):
    s_loc = fname.find('csv') - 3
    return int(fname[s_loc :s_loc + 1]) * 0.1

def plot_age_elevation(src_path, dst_path):
    for ea in ea_finder(src_path):
        print ea
        cols = ['ApatiteHeAge','Points:2', 'arc_length']
        frame1 = pnd.read_csv(ea, usecols = cols)
        if ea.find('riv') != -1:
            pic_name = name_dst_file(ea, dst_path, '_riv.png')
            df_res = df_ea_riv(frame1)
        else:
            pic_name = name_dst_file(ea, dst_path, '_esc.png')
            df_res = df_ea_esc(frame1)
        try:
            plot_ea(frame1, df_res, pic_name, uplift_from_fime_name(ea))
        except Exception, e:
            print 'error in file={0}, error msg = {1}'.format(ea, e.message)

if __name__ == '__main__':
    parser = ArgumentParser()
    #set rules
    parser.add_argument( "-src", dest="soure_path", help="source directory")
    parser.add_argument( "-dst", dest="dest_path", help="destination directory")

    kvargs = parser.parse_args()

    plot_age_elevation(kvargs.soure_path, kvargs.dest_path)

# src_path = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/'
# dst_path = '/home/imalkov/Dropbox/M.s/Research/PICTURES/AGE-ELEVATION/'