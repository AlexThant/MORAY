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
from numpy import matlib as matlib

plt.rcParams['figure.figsize']=[15,10]
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
def set_element_cross_section_on_centerline(X0, u, v, w, R_in :float, R_out :float, theta_resolution :int = 10) -> list[list[float,]]:

    """
    theta_resolution is in deg.
    x = X0 + R cos(theta) u1 + R sin(theta) v1
    y = Y0 + R cos(theta) u2 + R sin(theta) v2
    z = Z0 + R cos(theta) u3 + R sin(theta) v3
    """
    ntheta :int = np.int32(360 / theta_resolution) + 1
    x_bar_in : list[float] = np.empty(shape=ntheta) 
    y_bar_in : list[float] = np.empty(shape = ntheta)
    
    theta :list[float] = np.linspace(0, 2.*np.pi, num= ntheta, endpoint= True, dtype= np.float64) 

    x_bar_in = X0[0] + R_in * ( np.cos( theta ) * v[0] + np.sin( theta ) * w[0])
    y_bar_in = X0[1] + R_in * ( np.cos( theta ) * v[1] + np.sin( theta ) * w[1])
    
    x_bar_out = X0[0] + R_out * ( np.cos( theta ) * v[0] + np.sin( theta ) * w[0])
    y_bar_out = X0[1] + R_out * ( np.cos( theta ) * v[1] + np.sin( theta ) * w[1])
    
   # print(x_bar_in)
    #plt.plot(x_bar_in, y_bar_in)

    return x_bar_in, y_bar_in, x_bar_out, y_bar_out

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def create_surface_along_centerline(R_in :float=0.2, R_out :float= 0.5, ele_no :int = 40, theta_resolution :int = 30) -> list[list[float,]]:
    """
    Create the parametric surface using the position gradient coordinates
    """
    
    nodes :int = ele_no +1; ntheta:int = np.int32(360 / theta_resolution) + 1
    rP, rx, ry, rz = read_data_file(tsv_file, nodes)
    
    X_circ_in = np.empty(shape=(ntheta,nodes));  X_circ_out = np.empty(shape=(ntheta,nodes))
    Y_circ_in = np.empty(shape=(ntheta,nodes));  Y_circ_out = np.empty(shape=(ntheta,nodes))
    
    for i in range(nodes):
        X0 = rP[i,0:3];  u = rx[i, 0:3]; v = ry[i, 0:3]; w = rz[i, 0:3]
        X_circ_in[ :,i ], Y_circ_in[ :,i ], X_circ_out[ :,i ], Y_circ_out[ :,i ] = set_element_cross_section_on_centerline(X0, u, v, w, R_in, R_out, theta_resolution)
        
    #X_c = matlib.repmat(X_circ, nodes, 1)
    #Y_c = matlib.repmat(Y_circ, nodes, 1)
    
    X_in = X_circ_in + matlib.repmat(rP[:,0], ntheta, 1)
    Y_in = Y_circ_in + matlib.repmat(rP[:,1], ntheta, 1)
    X_out = X_circ_out + matlib.repmat(rP[:,0], ntheta, 1)
    Y_out = Y_circ_out + matlib.repmat(rP[:,1], ntheta, 1)
    
    Z = matlib.repmat(rP[:,2], ntheta, 1)
    
    return X_out, Y_out, X_in, Y_in, Z

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def end_caps():
    # Creating caps on both ends
    R = np.array([0,R])
    # cap at t=0
    X_cap, Y_cap, Z_cap = [p0[i] + np.outer(R, np.sin(theta)) * n1[i] + np.outer(R, np.cos(theta))*n2[i] for i in [0, 1, 2]]
    ax.plot_surface(X, Y, Z, edgecolors = "r", alpha=.4, linewidth = .1)
    # cap at t=mag
    X, Y, Z = [p0[i] + v[i]*mag + np.outer(R, np.sin(theta)) * n1[i] + np.outer(R, np.cos(theta))*n2[i] for i in [0, 1, 2]]
    ax.plot_surface(X, Y, Z, edgecolors = "r", alpha=.4, linewidth = .1)
    
    return

    
    

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def show_graphics_3D_pyplot(X, Y, X_in, Y_in, Z, title: str = 'Title', hollow_cylinder: bool = True,  background_transparency: bool = True, shrink_color_bar: bool = True) -> None:
    
    # Plot the surface
    fig = plt.figure()
    ax = fig.add_subplot(111, projection= '3d')
    surf = ax.plot_surface(X, Y, Z, color='k', cmap='rainbow', linewidth= 0.15, alpha= 1, antialiased= True, zorder=2) # rstride=1, cstride=1, cmap=cm.winter, linewidth=0.5, antialiased=True, zorder = 0.5)

    if hollow_cylinder:
        surf_1 = ax.plot_surface(X_in, Y_in, Z, color='k', cmap='rainbow', linewidth= 0.15, alpha= 1, antialiased= True, zorder=1)
        
    ax.contour(X,Y,Z)
    # Make legend, set axes limits and labels
    ax.legend()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-3, 0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Customize the view angle so it's easier to see the figure
    ax.view_init(elev=20., azim=-35, roll=0)

    ax.set_title(title)
    ax.set_aspect('equal')

    #ax.set(xticklabels=[],
    #   yticklabels=[],
    #   zticklabels=[])
    #ax.set_box_aspect([1.0, 1.0, 1.0])

    if background_transparency:
        # make the panes transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # make the grid lines transparent
        ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    if shrink_color_bar:
        cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
    else:
        cbar = fig.colorbar(surf)
    cbar.solids.set_edgecolor("face")

    # Show the plot
    plt.show()
    

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def show_graphics_mayavi(X, Y, X1, Y1, Z) -> None:
    import mayavi
    from mayavi import mlab
    
    title :str = '3D Parametric Surface:'
    #mlab.surf(Z, warp_scale='auto')
    mlab.clf()
    fig = mlab.mesh(X,Y,Z, representation='wireframe', color=(0,0,0))
    fig_1 = mlab.mesh(X1,Y1,Z, representation='wireframe', color=(0.5,0,1))
    mlab.axes(
                xlabel='x', ylabel='z', zlabel=title,
                x_axis_visibility=True, y_axis_visibility=True, z_axis_visibility=True
                )
    
    mlab.orientation_axes(xlabel='x', ylabel='z', zlabel=title)
    mlab.title(title)    
    #mlab.figure(figure=fig, bgcolor=(0, 0, 0), fgcolor=(0.5, 0.5, 0.5)); 
    mlab.outline()
    
    #mlab.figure(figure=fig_1, bgcolor=(0, 0, 0), fgcolor=(0.5, 0.5, 0.5))
    mlab.show()
    
    return None


if __name__ == '__main__':

    X,Y,X1,Y1,Z = create_surface_along_centerline()

   # X, Y = (xyz[:,0], xyz[:,1])
   # Z = matlib.repmat(xyz[:,2],len(X), 1)

    #show_graphics_3D_pyplot(X,Y,X1,Y1,Z)
    show_graphics_mayavi(X,Y,X1,Y1,Z)
