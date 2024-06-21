# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
#                   Created on Fri Jun 14 18:59:50 2024                       #
#                          @author: Thant Zin Htun                            #
#  >>>>>>>>>>> Bug report to :: tzhtun@naoe.eng.osaka-u.ac.jp <<<<<<<<<<<<<   #
#                       -*- ANCF Beam's visualizer -*-                        #
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#


import numpy as np
import sys

import  src.TSF_reader as TSF_READER
from src.Parametric_surfaces import ANCF_PIPE
from src.Plotter import DISPLAY


########### User inputs for setting #########
ele_num :int = 40
R_in :float = 0.01
R_ext :float= 0.03

##############################################


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  If you need modification to the script and have trouble getting it right, reach out to me. <<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Take the file as input
tsv_file = sys.argv[1]

if __name__ == '__main__':

    nodes_num :int = ele_num + 1
    Rp, R_x, R_y, R_z, n_display = TSF_READER.read_data_file(tsv_file, nodes_num)
    
    # Two flags for customized on and off settings
    flag : list[bool, bool]= [None]*2   
    
    flag[0] = ( True if (R_in != 0.)  else
                            False
                        )
    
    for id,_ in enumerate(n_display):
        
        l_start :int =  np.int32(id * nodes_num)  ; l_end :int = np.int32(id * nodes_num) + nodes_num
        
        rP = Rp [ l_start:l_end,: ]
        rx = R_x[ l_start:l_end,: ]
        ry = R_y[ l_start:l_end,: ]
        rz = R_z[ l_start:l_end,: ]
        
        
        try:
            flag[1] = (True if (id == len(n_display) -1)  else
                      False
                      )
                      
            #__________ solid flexible pipe ____________
            if (R_in == 0.):
                X, Y, Z, Xcrs_t, Ycrs_t, Zcrs_t, Xcrs_b, Ycrs_b, Zcrs_b = ANCF_PIPE.create_surface_along_centerline(rP, rx, ry, rz, R_in, R_ext, nodes= nodes_num)
                 
                surf = DISPLAY.pyplot_3d_surface( X, Y, Z, 
                                                 Xcrs_t, Ycrs_t, Zcrs_t, 
                                                 Xcrs_b, Ycrs_b, Zcrs_b, 
                                                 X_in, Y_in, 
                                                 setting_flag= flag, plot_id= id, colormap_variable= 'deformation' 
                                                )
            else:
            #__________ hollow flexible pipe ____________
                X, Y, Z, Xcrs_t, Ycrs_t, Zcrs_t, Xcrs_b, Ycrs_b, Zcrs_b, X_in,Y_in = ANCF_PIPE.create_surface_along_centerline(rP, rx, ry, rz, R_in, R_ext, nodes= nodes_num)
                
                surf = DISPLAY.pyplot_3d_surface( X, Y, Z,
                                                 Xcrs_t, Ycrs_t, Zcrs_t, 
                                                 Xcrs_b, Ycrs_b, Zcrs_b,
                                                 X_in, Y_in,
                                                 setting_flag= flag, plot_id= id, colormap_variable= 'deformation' 
                                                )
            
        except NotImplementedError  as err:
            print(f"%s Return values error. %s", err)   
        
         
        #show_graphics_mayavi( X, Y, Z, Xcrs_t, Ycrs_t, Zcrs_t, Xcrs_b, Ycrs_b, Zcrs_b, X_in, Y_in )

    DISPLAY.pyplot_settings_helper(surf, title=None)
    DISPLAY.save_fig('Drill_pipe_demo_display.png')
    DISPLAY.show_fig()
