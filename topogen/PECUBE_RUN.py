import math
import os
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy
import imp
import subprocess
import time
import datetime

class ListTable(list):
    """ Overridden list class which takes a 2-dimensional list of 
        the form [[1,2,3],[4,5,6]], and renders an HTML Table in 
        IPython Notebook. """
    
    def _repr_html_(self):
        html = ["<table>"]
        for row in self:
            html.append("<tr>")
            
            for col in row:
                html.append("<td>{0}</td>".format(col))
            
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

#original haversine formula
def haversine(lon1, lon2, lat1 ,lat2):
    R = 6372.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
     
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

    #calculate 1 km in deg relative to given lon-lat
def kmUnit(lon, lat, tol, initval):
    delta = 0
    del_inc = 0.00001
    while(abs(initval-1)>tol):
        delta = delta + del_inc
        initval = haversine(lon, lon+delta, lat ,lat+delta)
    return delta

    
############################################################################################################
def calcTopo(nx, ny, foo):
    X = numpy.arange(0, nx, 1)
    Y = numpy.arange(0, ny,1)
    X, Y = numpy.meshgrid(X, Y)
    zs = numpy.array([foo(x,y) for x,y in zip(numpy.ravel(X), numpy.ravel(Y))])
    Z = zs.reshape(X.shape)
    return (X,Y,Z)
#------------------------------------------------------------------------------------------------------------
def calcTopo2(foo,nx,ny,ystrt,h,tangle,scale,angscale):
    X = numpy.arange(0, nx, 1)
    Y = numpy.arange(0, ny,1)
    X, Y = numpy.meshgrid(X, Y)
    zs = numpy.array([foo(x,y,ystrt,h,tangle,scale,angscale) for x,y in zip(numpy.ravel(X), numpy.ravel(Y))])
    Z = zs.reshape(X.shape)
    return (X,Y,Z)

def cascadeTopo(foo,nx,ny,ystrt,h,tangle):
    pass
#------------------------------------------------------------------------------------------------------------
def genTopoFig(X,Y,Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    try:
        ax.set_xlabel('Width')
        ax.set_ylabel('Length')
        ax.set_zlabel('Hight')
        #ax.set_xticks([])
        #ax.set_yticks([])
        ax.set_zticks([])
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()
    except Exception, e:
        print "Error in Fig Creation" 
#--------------------------------------------------------------------------------------------------------------
def writeToTopofname(data, ptxt):
    try:
        numpy.savetxt(ptxt, data.flatten(),fmt='%d')
    except Exception,e:
        print "Error in Print" + str(e)
#--------------------------------------------------------------------------------------------------------------
def savedata(fpath,backupfold = 'VTK_OLD'):
    subprocess.call('rm '+fpath+'peout/*.*',shell=True) #clear peout
    subprocess.call('mkdir '+fpath+backupfold,shell=True) #make new directiry
    subprocess.call('mv '+fpath+'VTK/*.* '+fpath+backupfold+'/',shell=True) #mv vtk files

    return ('','')
#--------------------------------------------------------------------------------------------------------------
def exeshcmd(mdpath,shcommand,inflag = False):
    err_ans = []
    out_ans = []
    pdir = os.getcwd()
    os.chdir(mdpath)
    
    p = subprocess.Popen(shcommand, stdin=subprocess.PIPE,stderr = subprocess.PIPE,stdout = subprocess.PIPE)
    # p = subprocess.Popen(shcommand,shell='/bin/bash', stdin=subprocess.PIPE,stderr = subprocess.PIPE,stdout = subprocess.PIPE)
    if(inflag == True):
        time.sleep(2)
        print >>p.stdin,'peout'
        p.stdin.close()
    p.wait()
    
    os.chdir(pdir)
    for line in iter(p.stderr.readline, b''):
        err_ans.append(line)
    for line in iter(p.stdout.readline, b''):
        out_ans.append(line)

    return (''.join(out_ans),''.join(err_ans))

################## running code ###########################################
# from subprocess import Popen
# expath  = '/home/imalkov/Dropbox/CODE/myprog'
# cmds = [[expath, 'a','/home/imalkov/Dropbox/CODE/myprog1/out.txt'], \
# [expath, 'b','/home/imalkov/Dropbox/CODE/myprog2/out.txt'], \
# [expath, 'c','/home/imalkov/Dropbox/CODE/myprog3/out.txt']]
# processes = [Popen(cmd) for cmd in cmds]
# for proc in processes:
#     proc.wait()
################################################################################################
pecexe = {
    'ClearDir': lambda a : savedata(a,'VTK_'+ (datetime.datetime.now().isoformat()).replace(':','_')), 
    'Test': lambda a: exeshcmd(a,"./bin/Test"),
    'Pecube': lambda a: exeshcmd(a,"./bin/Pecube"),
    'Vtk': lambda a: exeshcmd(a,"./bin/Vtk",True),
    'All': lambda a: map(lambda op: exeshcmd("./bin/"+op,True) if op == 'Test' else exeshcmd("./bin/"+op),['Test','Pecube','Vtk'])
   }

############## Topography ######################################

def zeroSurfe(xsize,ysize):
    return genMGSurfe(xsize,ysize,lambda xi,yi: 0*xi + 0*yi)

def genMGSurfe(xsize,ysize,foo):
    x  = numpy.linspace(0, xsize, xsize)
    y  = numpy.linspace(0, ysize ,ysize)
    xi,yi = numpy.meshgrid(x,y)
    return foo(xi,yi)