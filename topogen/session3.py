__author__ = 'imalkov'

import pandas as pnd
import matplotlib.pylab as plt
import numpy as np



def get_yticks(min, max):
    global txs
    global lebs
    txs = np.linspace(np.round(min), np.ceil(max), 11)
    lebs = ['0'] + [str(i) for i in txs[1:]]
    lebs.reverse()

def plot_age_elevation(f, ax):
    frame1 = pnd.read_csv(f, usecols = ['ApatiteHeAge','Points:2'])

    fd = frame1[(frame1['Points:2'] < max(frame1['Points:2']))
             & (frame1['Points:2'] > min(frame1['Points:2']))]

    fd['Elevation'] = fd['Points:2'] - min(frame1['Points:2'])
    get_yticks(min(fd['Elevation']), max(fd['Elevation']))
    return fd.plot(x = 'ApatiteHeAge', y = 'Elevation', style = '-o', ax = ax)

def name_dst_file(fname):
    node_loc = fname.find('NODE') + len('NODE')
    s_loc = fname.find('csv') - 3
    return  'n{0}s{1}'.format(fname[node_loc:node_loc + 2], fname[s_loc:s_loc + 2])



