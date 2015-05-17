
from pecuberun import *
import numpy as np

def zeroSurfe(xsize,ysize):
    return gen_mgsurf(mrow,mcol,lambda xi,yi: 0)

def genMGSurfe(xsize,ysize,foo):
    x  = np.linspace(0, xsize, xsize)
    y  = np.linspace(0, ysize ,ysize)
    xi,yi = np.meshgrid(x,y)
    return foo(xi,yi)

#resolution of 101 m = 0.00067 angle
#------------------------------------
#grid size
mrow = 453# -> 30 km 
mcol = 808 # -> 60 km 

#------------------------------------
#fault geometry
fylocation = mcol/2 #location on grid
fang = 60 # fault angle
#------------------------------------
#canyon geometry
cynlocation = mrow / 2
#------------------------------------
# ----------------------------------------------------------- #
# ---------------------0 Ma Topography -------------------- #
# ----------------------------------------------------------- #

#step0 - start topography is flat

# ----------------------------------------------------------- #
# CODE
st0 = zeroSurfe(xsize,ysize)

# ----------------------------------------------------------- #
# --------------------- 20 Ma Topography -------------------- #
# ----------------------------------------------------------- #

#step1 - 20 Ma of no uplift (flat topography)

# ----------------------------------------------------------- #
# CODE
st1 = gen_mgsurf(mrow,mcol,lambda xi,yi: 0)

# ----------------------------------------------------------- #
# --------------------- 40 Ma Topography -------------------- #
# ----------------------------------------------------------- #
#step2 - 20 Ma of constant uplift U = 0.2 km / Ma that will generate 20*0.2*sin(60) topography heght
# and generate canyon with 0.05 slope at the Footwall toward the escarpment + 30 deg 
#maxh = 20*0.2*np.sin(np.deg2rad(60)) ; print maxh

# ----------------------------------------------------------- #
# CODE

#canyon slope

zl = gen_mgsurf(mrow / 2,mcol / 2,lambda xi,yi: 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0.05)) * yi)
z = np.concatenate((np.fliplr(zl),zl),axis=1)
z = np.hstack((z,np.zeros((z.shape[0],1))+fwmaxh)) #add column
#escarpment
st2 = gen_mgsurf(mrow,fylocation,lambda xi,yi: 101 * np.tan(np.deg2rad(60)) * yi)
#final topography
st2[z<st2] = z[z<st2]
st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)
st2[st2 > fwmaxh] = 200 * 20 * np.sin(np.deg2rad(60)) # footwall maximum height (4 km = 4000 m)
# END CASE
# ----------------------------------------------------------- #


# <codecell>

#resolution of 101 m = 0.00067 angle
#------------------------------------
#grid size
mrow = 453# -> 30 km 
mcol = 808 # -> 60 km 
flwf = 0
maindir = '/home/imalkov/Dropbox/M.s/Research/DATA/SESSION_TREE/'
#------------------------------------
#fault geometry
fylocation = mcol/2 #location on grid
fang = 60 # fault angle
#------------------------------------
#canyon geometry
cynlocation = mrow / 2
#------------------------------------
if flwf == 0:
    fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
# ----------------------------------------------------------- #
# ---------------------0 Ma Topography -------------------- #
# ----------------------------------------------------------- #

#step0 - start topography is flat

# ----------------------------------------------------------- #
# CODE

st0 = numpy.zeros((mrow,mcol))
if(flwf == 0):
    im1 = ax1.imshow(st0.T, interpolation='none')
elif(flwf == 1):
    write_topo_fname(st0.T,maindir+'/step0.txt')
else:
    pass
# ----------------------------------------------------------- #
# --------------------- 20 Ma Topography -------------------- #
# ----------------------------------------------------------- #

#step1 - 20 Ma of no uplift (flat topography)

# ----------------------------------------------------------- #
# CODE
st1 = numpy.zeros((mrow,mcol))

if(flwf == 0):
    im2 = ax2.imshow(st1.T, interpolation='none')
elif flwf == 1:
    write_topo_fname(st1.T,maindir+'/step1.txt')
else:
    pass

# ----------------------------------------------------------- #
# --------------------- 40 Ma Topography -------------------- #
# ----------------------------------------------------------- #
#step2 - 20 Ma of constant uplift U = 0.2 km / Ma that will generate 20*0.2*sin(60) topography heght
# and generate canyon with 0.05 slope at the Footwall toward the escarpment + 30 deg 
#maxh = 20*0.2*np.sin(np.deg2rad(60)) ; print maxh

# ----------------------------------------------------------- #
# CODE

#canyon slope

fwmaxh = 200 * 20 * np.sin(np.deg2rad(fang)) # footwall maximum height (4 km = 4000 m)

x  = np.linspace(0,(mrow) / 2, (mrow)/ 2)
y  =  np.linspace(0,fylocation , fylocation)
xi,yi = np.meshgrid(x,y)
zl = 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0.01)) * yi
zl[zl > fwmaxh] = fwmaxh
zr = np.fliplr(zl)

z = np.concatenate((zr,zl),axis=1)
z = np.hstack((z,np.zeros((z.shape[0],1))+fwmaxh)) #add column

#escarpment
xe  = np.linspace(0,mrow, mrow)
ye  =  np.linspace(0,fylocation , fylocation)

xei,yei = np.meshgrid(xe,ye)

st2 = 101 * np.tan(np.deg2rad(60)) * yei
st2[st2 > fwmaxh] = fwmaxh

#final topography
st2[z<st2] = z[z<st2]

st2 = np.concatenate((np.zeros(st2.shape),st2),axis=0)

if(flwf == 0):
    im3 = ax3.imshow(st2, interpolation='none')
elif flwf == 1:
    write_topo_fname(st2,maindir+'/step2.txt')
elif flwf == 2:
    plt.imshow(st2, interpolation='none')
else:
    pass

# ----------------------------------------------------------- #
# --------------------- 60 Ma Topography -------------------- #
# ----------------------------------------------------------- #
#step2 - 20 Ma of constant uplift U = 0.2 km / Ma that will generate 20*0.2*sin(60) topography heght
# and generate canyon with 0.05 slope at the Footwall toward the escarpment + 30 deg 
#maxh = 20*0.2*np.sin(np.deg2rad(60)) ; print maxh

# ----------------------------------------------------------- #
# CODE

#canyon slope

fwmaxh = 200 * 20 * np.sin(np.deg2rad(60)) # footwall maximum height (4 km = 4000 m)

x  = np.linspace(0,(mrow) / 2, (mrow)/ 2)
y  =  np.linspace(0,fylocation , fylocation)
xi,yi = np.meshgrid(x,y)
zl = 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0.05)) * yi
zl[zl > fwmaxh] = fwmaxh
zr = np.fliplr(zl)

z = np.concatenate((zr,zl),axis=1)
z = np.hstack((z,np.zeros((z.shape[0],1))+fwmaxh)) #add column

#escarpment
xe  = np.linspace(0,mrow, mrow)
ye  =  np.linspace(0,fylocation , fylocation)

xei,yei = np.meshgrid(xe,ye)

st3 = 101 * np.tan(np.deg2rad(20)) * yei
st3[st3 > fwmaxh] = fwmaxh

#final topography
st3[z<st3] = z[z<st3]
st3 = np.concatenate((np.zeros(st3.shape),st3),axis=0)

if(flwf == 0):
    im3 = ax3.imshow(st3, interpolation='none')
elif flwf == 1:
    write_topo_fname(st3,maindir+'/step3.txt')
elif flwf == 2:
    plt.imshow(st3, interpolation='none')
else:
    pass
   
# ----------------------------------------------------------- #
# ----------------------------------------------------------- #
# PRINT CASE

if flwf == 0:
    fig.show()
else:
    pass

# END CASE
# ----------------------------------------------------------- #

# <codecell>

st3.shape

# <codecell>


