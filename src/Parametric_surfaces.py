# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
#                   Created on Thu Jun 20 19:56:30 2024                       #
#                          @author: Thant Zin Htun                            #
#                        tzhtun@naoe.eng.osaka-u.ac.jp                        #
#                       -*- ANCF Beam's visualizer -*-                        #
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#

import numpy as np
from numpy import matlib as matlib

class ANCF_PIPE:
    def __init__(self) -> None:
        return None
      
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def create_element_cross_section_on_centerline(self, R_ext :float, u :list[float,], v :list[float], w :list[float,], theta :list[float], ntheta :int = 10) -> list[list[float,]]:
        """
        theta_resolution is in deg.
        x = X0 + R cos(theta) u1 + R sin(theta) v1
        y = Y0 + R cos(theta) u2 + R sin(theta) v2
        z = Z0 + R cos(theta) u3 + R sin(theta) v3
        """
        rP_bar_circ : list[float] = np.empty(shape= ( ntheta,3 )) 
        
        rP_bar_circ[:,0], rP_bar_circ[:,1], rP_bar_circ[:,2] = [ R_ext * ( np.cos( theta ) * v[i] + np.sin( theta ) * w[i]) for i in range(3) ]
        
        return rP_bar_circ[:,0], rP_bar_circ[:,1], rP_bar_circ[:,2]

    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def create_surface_along_centerline(self, rP : list[float,], rx : list[float,], ry : list[float,], rz : list[float,], R_in :float=0.02, R_ext :float= 0.035, nodes :int = 1, theta_resolution :int = 30) -> list[list[float,]]:
        """Create the parametric surface using the position gradient coordinates

        Args:
            R_in (float, optional): _description_. Defaults to 0.3.
            R_ext (float, optional): _description_. Defaults to 0.5.
            ele_no (int, optional): _description_. Defaults to 1.
            theta_resolution (int, optional): _description_. Defaults to 30.

        Returns:
            list[list[float,]]: _description_
        """  
        
        ntheta:int = np.int32(360 / theta_resolution) + 1
        
        theta :list[float] = np.linspace(0, 2.*np.pi, num= ntheta, endpoint= True, dtype= np.float64)
        
            
        X_circ = np.empty(shape=(ntheta,nodes));  
        Y_circ = np.empty(shape=(ntheta,nodes));  
        Z_circ = np.empty(shape=(ntheta,nodes))
        
        
        if (R_in != 0.):
            X_circ_in = np.empty(shape=(ntheta,nodes)); Y_circ_in = np.empty(shape=(ntheta,nodes))
            
        
        for i in range(nodes):
            X0 = rP[ i,: ];  u = rx[ i,: ]; v = ry[ i,: ]; w = rz[ i,: ]
            X_circ[ :,i ], Y_circ[ :,i ], Z_circ[ :,i ]= self.create_element_cross_section_on_centerline(R_ext, u, v, w, theta, ntheta)
            
            if (i == 0):  # at 0th Node
                Xcrs_0, Ycrs_0, Zcrs_0 = self.create_end_caps(R_in, R_ext, X0, u, v, w, theta)

            if (i == nodes-1):   # at nth Nodes
                Xcrs_n, Ycrs_n, Zcrs_n = self.create_end_caps(R_in, R_ext, X0, u, v, w, theta)


        #X_c = matlib.repmat(X_circ, nodes, 1)
        #Y_c = matlib.repmat(Y_circ, nodes, 1)
        
        if (R_in == 0.):
            
            X_circ[ :,: ] += X0[0] ;  Y_circ[ :,: ] += X0[1]
            X = X_circ + matlib.repmat(rP[ 0:nodes,0 ], ntheta, 1)
            Y = Y_circ + matlib.repmat(rP[ 0:nodes,1 ], ntheta, 1)
            Z = matlib.repmat(rP[ 0:nodes,2 ], ntheta, 1)
            
            return X, Y, Z, Xcrs_0, Ycrs_0, Zcrs_0, Xcrs_n, Ycrs_n, Zcrs_n
        
        else:
            
            X_circ_in = X_circ[ :,: ]* R_in / R_ext + X0[0] ; Y_circ_in = Y_circ[ :,: ]* R_in / R_ext + X0[0] 
            X_circ[ :,: ] += X0[0] ;  Y_circ[ :,: ] += X0[1]
            
            X = X_circ + matlib.repmat(rP[ 0:nodes,0 ], ntheta, 1)
            Y = Y_circ + matlib.repmat(rP[ 0:nodes,1 ], ntheta, 1)
            Z = matlib.repmat(rP[ 0:nodes,2 ], ntheta, 1)
            
            X_in = X_circ_in + matlib.repmat(rP[ 0:nodes,0 ], ntheta, 1)
            Y_in = Y_circ_in + matlib.repmat(rP[ 0:nodes,1 ], ntheta, 1)
            
            return X, Y, Z, Xcrs_0, Ycrs_0, Zcrs_0, Xcrs_n, Ycrs_n, Zcrs_n, X_in, Y_in

    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def create_end_caps(self, R_in :float = 0., R_ext :float = 1., 
                        rP:list[float]= None,  rx:list[float]= None, ry:list[float]= None, rz:list[float]= None, 
                        theta :list[float]= None
                        ):
        """Create end caps of the pipe using the nodal coordinates of ANCF beam.

        Args:
            R_in (float): _description_
            R_ext (float): _description_
            rP (list[float]): _description_
            theta (list[float]): _description_
        """
        # Creating caps on both ends
        R = np.array([R_in,R_ext]); 

        X_cap, Y_cap, Z_cap = [ rP[i] + np.outer(R, np.sin(theta)) * ry[i] + np.outer(R, np.cos(theta))*rz[i] for i in range(3) ]
        
        return X_cap, Y_cap, Z_cap
    

# Object lists
ANCF_PIPE = ANCF_PIPE()

if __name__ == '__main__':
    raise Exception("Running this script as a standalone module is not allowed.")