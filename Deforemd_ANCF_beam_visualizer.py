# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
#                   Created on Fri Jun 14 18:59:50 2024                       #
#                          @author: Thant Zin Htun                            #
#                                                                             #
#                       -*- ANCF Beam's visualizer -*-                        #
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#


import numpy as np, scipy as sp             # for scientific computing
import matplotlib; matplotlib.use('TkAgg')  # for compatibility on Mac OS
import matplotlib.pyplot as plt             # for generating plots & graphs
import os,sys
import csv
import mayavi
from mayavi import mlab

plt.rcParams['figure.figsize']=[12,8]
plt.rcParams.update({'font.size': 12})
#

# Take the file as input
tsv_file = sys.argv[1]

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def read_data_file(tsv_file :str|os.PathLike, nodes :int, beam_DoFs :int = 24) -> list[list[float,]]:
    """ 
    Reads the tab separated data file for the beam's configuration at a selected time step.
    input (required):: No. of DoFs of a single element (e.g. Default value :: 24 for a 3D-fully-parameterized ANCF beam).
    """

    # Create an empty multi-diimensional array using NUMPY.
    
    arr_size :tuple = (nodes,3)

    rP : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
    rx : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
    ry : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
    rz : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)

    with open(tsv_file, "r") as f:
        #Read .csv file column by column
        col_count :int = 0; 

        for column in zip(*[line for line in csv.reader(f, dialect="excel-tab")]): # csv.reader(f, delimiter="\t")
            nc_index :int = np.int32(col_count % 3)

            
            if (col_count < 3): 
                rP[0:len(column), nc_index] = column 

            elif (3 <= col_count < 6):
                rx[0:len(column), nc_index] = column 

            elif (6 <= col_count < 9):
                ry[0:len(column), nc_index] = column 

            elif (9 <= col_count <= 11):
                rz[0:len(column), nc_index] = column 

            col_count +=1

    return rP, rx, ry, rz

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def set_cross_section_on_center_line(R_in :float=0, R_out :float= 0.5, ele_no :int = 40, theta_resolution :int = 10) -> list[list[float,]]:

    """
    theta_resolution is in deg.
    x = X0 + R cos(theta) u1 + R sin(theta) v1
    y = Y0 + R cos(theta) u2 + R sin(theta) v2
    z = Z0 + R cos(theta) u3 + R sin(theta) v3
    """
    nodes :int = ele_no +1; theta_divisions :int = np.int32(360 / 10) + 1
    xyz_coord_in : list[list[float], list[float], list[float]]= np.empty(shape = (theta_divisions,3))
    xyz_coord_out : list[list[float], list[float], list[float]]= np.empty(shape = (theta_divisions,3))
    theta_list :list[float] = np.linspace(0, 2.*np.pi, num= theta_divisions, endpoint= True, dtype= np.float64) 

    rP, rx, ry, rz = read_data_file(tsv_file, nodes)
    X0= rP[20, 0:3]; u = ry[20, 0:3]; v = rz[20, 0:3]; w = rx[20, 0:3]

    for row, theta in enumerate(theta_list):
        for col in range(3):

            #xyz_coord_in[row, col] = X0[col] + R_in * ( np.cos( theta ) * u[col] + np.sin( theta ) * v[col])
            xyz_coord_out[row, col] = X0[col] + R_out * ( np.cos( theta ) * u[col] + np.sin( theta ) * v[col])


    return xyz_coord_out#, xyz_coord_out
    

if __name__ == '__main__':

    xyz = set_cross_section_on_center_line()

    X, Y = (xyz[:,0], xyz[:,1])
    Z = xyz[:,2]

    print(X)
    #Z = np.reshape(z, X.shape)
    #mlab.surf(X, Y, Z, extent=(0,1,0,1,0,1))

        #mlab.surf(Z, warp_scale='auto')
    #mlab.plot3d(X,Y,Z)
    #mlab.show()

    # Plot the surface
    #ax = plt.axes(projection='3d')
    #ax.plot_surface(X, Y, xyz[:,2], cmap='viridis')
    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=cm.Blues)

    #ax.set(xticklabels=[],
    #   yticklabels=[],
    #   zticklabels=[])
    #plt.show()
