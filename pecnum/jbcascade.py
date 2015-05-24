__author__ = 'imalkov'
import numpy as np
# from matplotlib import cm
import matplotlib.pylab as plt
from scipy.spatial import Voronoi, Delaunay,  voronoi_plot_2d

# c OUTPUT: dt             = (initial) time step length (in yr)
# c         iadjust        = allows for dynamic time stepping (=0
# c                          means that time step is fixed; =1 means
# c                          that time step is adjusted dynamically)
# c         endtime        = final time (in yr)
# c         ishow          = frequency of graphic displays (in time steps)
# c         writetime      = frequency of output (in yr)
# c         nshortwrite    = frequency of short screen output (in time steps)
# c         iflux          = frequency of flux saves (=0 no flux save;
# c                          otherwise frequency in time steps); this output
# c                          is of total flux through the fixed nodes
# c         run_name       = name of this run; must also be the name
# c                          of an existing folder where all output files
# c                          will be stored
# c         iadapt         = flag to allow dynamic remeshing (=0 no; =1 yes)
# c         surfmin        = minimum surface area that can be reached by
# c                          remeshing/refining
# c         ihorizontal    = flag to permit horizontal mesh movement (=0
# c                          means no horizontal movement; =1 means horizontal
# c                          movements permitted
# c         iflexure       = flag to permit flexural isostasy (=0 no flexure;
# c                          =1 flexure)
# c         hflex          = size (in m) of the square mesh on which the
# c                          thin elastic plate calculations are done
# c         ixflex         = flag to permit flexure in the x-direction
# c                          (=0 no elastic strength in x-direction;
# c                          =1 means elastic strength in x-direction)
# c         iyflex         = flag to permit flexure in the y-direction
# c                          (=0 no elastic strength in y-direction;
# c                          =1 means elastic strength in y-direction)
# c         thickflex      = elastic thickness in m
# c         ym             = Young Modulus (in Pa)
# c         pratio         = Poissons's ratio
# c         rhocflex       = crustal density (in kg/m**3)
# c         rhoaflex       =asthenospheric density (in kg/m**3)
# c         oro_length     = orographic length scale (in m)
# c                          (=0 means no orographic control on precipitation)
# c         oro_height     = orographic height scale (in m)
# c         oro_scale      = background precipitation (in adequate units)
# c         wind_direction = wind direction (0= along x-axis)
# c         xlf_AL         = fluvial erosion length scale for alluvials
# c                          (in m)
# c         sea_level      = where sea-level is (in m above the 0 datum)
# c                          below sea-level no sediment transport is
# c                          allowed
# c         ideposition    = flag to allow for fluvial deposition (=0 erosion
# c                          only; =1 sedimentation allowed)
# c         idiffusion     = flag to allow diffusion processes (=0 no
# c                          diffusion; =1 diffusion allowed)
def init_gen_params(context):
    context.gen_params = {'dt':0, 'iadjust':0 , 'endtime':0}
    return context

 #  parameter (nnodemax=300*300,nparam=4,nmemory=7,
 # &          nbmax=20,ntmax=20,nflex=256,nx = 176,
 # &          ny = 251,hwlim=119)
 #      real       x(nnodemax),y(nnodemax),hi(nnodemax)
 #      real       h(nnodemax),h0(nnodemax)

def init_nodal_geomety(nnode, nx, ny, context):
    context.nodal_geometry = {}
    return context

def find_neighbours(points):

    # points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],[2, 0], [2, 1], [2, 2]])
    vor = Voronoi(points)
    voronoi_plot_2d(vor)
    plt.show()

if __name__ == '__main__':
    # sidex = 180.e3
    # sidey = 250.e3

    ny = 200#808
    nx = 50#453
    hw_half = ny/2
    mat = np.ones((nx, ny))

    # print(nx*hw_half)
    matf = mat.flatten()
    for j in range(ny):
        for i in range(nx):
            inode = j*nx+i
            # print(inode)
            # print(nx * j + hw_half)
            if inode < (nx * hw_half):
                matf[inode] = 0
            if j == 0 or j == (ny - 1):
                matf[inode] = 0
            if i == 0 or i == (nx - 1):
                matf[inode] = 0

            # if i == (nx - 1) and inode < j*nx + i:
            #     mat[i,j] = 10
            # if i == 0 and inode < i*ny + j:
                # mat[i ,j] = 0
                # print('hello')

    matf = matf.reshape((ny,nx))
    plt.imshow(matf.T)
    plt.show()
    # nnode = 453 * 808

    # x = np.linspace(0, 30, 453)
    # y = np.linspace(0, 60, 808)
    #
    # grid = []
    # for i in range(4):
    #     for j in range(8):
    #         grid.append([i,j])


    # grid = np.indices((453,808,3))
    # print(grid[0])
    # find_neighbours(grid)

    # xi, yi = np.meshgrid(x, y)
    # s = xi*sidex + 500 * (xr*2-1) + yi*sidey + 500*(xr*2-1)
    # print(xi[0,:])

    # h = np.random.rand(453, 808)
    # h0 = h
    # hi = h

    # plt.imshow(h)
    # print s.shape
    # plt.show()

    # zl = gen_mgsurf(cynlocation, fylocation, lambda xi,yi: 101 * np.tan(np.deg2rad(30)) * xi + 101 * np.tan(np.deg2rad(0)) * yi)
    # z = np.random.rand(len(x),len(y))
    # plt.imshow(z)
    # plt.show()


