__author__ = 'imalkov'

import numpy as np
import matplotlib.pylab as plt
import collections
import os
import sys

cmap = {
        30:'b',
        35:'g',
        40:'r',
        45:'c',
        50:'m',
        55:'k',
        60:'y'}

fmap = {}

#service
def mapDistToXY(XInd, YInd, DInd, fname, d, cont_x = lambda x,y: x, cont_y = lambda x,y: y):
    ''' Read pair of columns as value in dictionary and map it (the pair) to key value
        where on every element in pair continuation is applied.

        Input:

        Output:

    '''
    try:
    #map index
        AllArr = np.loadtxt(fname, delimiter=',', skiprows=1)

        YArr = cont_y(AllArr[:,XInd],AllArr[:,YInd])
        XArr = cont_x(AllArr[:,XInd],AllArr[:,YInd])

        if d.has_key(AllArr[0,DInd]) == False:
            d[AllArr[0,DInd]] = (XArr,YArr)
        else:
            d[AllArr[0,DInd]] = (d[AllArr[0,DInd]],(XArr,YArr))
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
        print "Could not convert data to an integer."
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return

def recPlotDict(key,val,ax,ppat = '-'):
    '''
    Input:

    Output:

    '''
    #base
    global fmap
    x,y = val

    if type(x) != tuple and type(y) != tuple:
        if fmap[key] == False:
            ax.plot(x,y,ppat + cmap[key],label = str(key) + ' km')
            fmap[key] = True;
        else:
            ax.plot(x,y,ppat + cmap[key])
    elif type(x) == tuple and type(y) == tuple:
        recPlotDict(key,x,ax,ppat); recPlotDict(key,y,ax,ppat)

    else:
        print "TUPLE ERROR"
        exit()

    return

def PlotDict(d,ppat = '-'):
    '''
        Input:

        Output:

    '''
    #set fmap
    global fmap
    for i in range(30,61,5):
        fmap[i] = False

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    od = collections.OrderedDict(sorted(d.items()))
    for key,val in od.iteritems():
        recPlotDict(key,val,ax,ppat)
    return ax,fig

def MngPlot(ax,xlbl,ylbl,tlt):
    ax.set_xlabel(xlbl)
    ax.set_ylabel(ylbl)
    ax.set_title(tlt,fontsize=18,fontname="Times New Roman")
    ax.grid()
    legend = ax.legend(loc='best', shadow=True, bbox_to_anchor=(1, 1),fancybox=True,ncol=1)


    frame = legend.get_frame()
    frame.set_facecolor('0.95')

    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width

    return

csvdir = '/home/imalkov/Documents/Session1/Session1A/CSV/'
if os.path.exists(csvdir) is False:
    sys.exit()

Iso50cProfiles = 'Iso50cProfiles'
ext = '.csv'
d = {}

for i in range(6):
    fname = csvdir + Iso50cProfiles + str(i) + ext
    mapDistToXY(6, 9, 8, fname, d)

ax,fig = PlotDict(d)
MngPlot(ax,'Block Length [km]','Isotherma Depth [km]','Isotherma 50c')