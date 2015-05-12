__author__ = 'imalkov'

import pandas as pnd
import matplotlib.pylab as plt
import numpy as np

txs = []
lebs = []

def get_yticks(min, max):
    global txs
    global lebs
    txs = np.linspace(np.round(min), np.ceil(max), 11)
    # txs = np.linspace(0, -5, 11)
    lebs = ['0'] + [str(i) for i in txs[1:]]
    lebs.reverse()

def plot_age_elevation(f, ax):
    frame1 = pnd.read_csv(f, usecols = ['ApatiteHeAge','Points:2'])

    fd = frame1[(frame1['Points:2'] < max(frame1['Points:2']))
             & (frame1['Points:2'] > min(frame1['Points:2']))]

    fd['Elevation'] = fd['Points:2'] - min(frame1['Points:2'])
    get_yticks(min(fd['Elevation']), max(fd['Elevation']))
    return fd.plot(x = 'ApatiteHeAge', y = 'Elevation', style = '-o', ax = ax)

def name_ae_file(fname):
    node_loc = fname.find('NODE') + len('NODE')
    s_loc = fname.find('csv') - 3
    return  'n{0}s{1}'.format(f[node_loc:node_loc + 2], fname[s_loc:s_loc + 2])

#code


save_dir = '/home/imalkov/Dropbox/M.s/Research/PICTURES/AGE-ELEVATION'
flist = ['/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session2A/csv/Age-Elevation0.csv',
         '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02/Session1A/csv/Age-Elevation0.csv']



f = plt.figure()
ax = f.gca()

for f in flist:
    ax =  plot_age_elevation(f, ax)

print txs
plt.title('Age-Elevation')
plt.xlabel('ApatiteHeAge [Ma]')
plt.ylabel('Elevation [Km]')
plt.legend(['U=0.2 mm/y, Ex=0','U=0.1 mm/y, Ex=0'], loc='best' , fontsize=10)
plt.yticks(txs, lebs)
# plt.show()
plt.savefig('{0}/{1}_ae.png'.format(save_dir, '_'.join([name_ae_file(n) for n in flist])))

