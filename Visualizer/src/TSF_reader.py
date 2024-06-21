# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
#                   Created on Fri Jun 14 18:59:50 2024                       #
#                          @author: Thant Zin Htun                            #
#                        tzhtun@naoe.eng.osaka-u.ac.jp                        #
#                       -*- ANCF Beam's visualizer -*-                        #
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#

import numpy as np
import os
import csv

# __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
def read_data_file(tsv_file :str|os.PathLike, nodes :int, beam_DoFs :int = 24) -> list[list[float,]]:
    """ 
    Reads the tab separated data file for the beam's configuration at a selected time step.
    input (required):: No. of DoFs of a single element (e.g. Default value :: 24 for a 3D-fully-parameterized ANCF beam).
    """
    
    keyword_to_visualize = "Visualize"
    with open(tsv_file, "r") as f:
        
         # /* Read the first header line of input .txt file containing the ANCF beam's nodal coordinates.            
            
        lines :list[str] = [line for line in csv.reader(f, dialect="excel-tab")]
        
        visualization_str_items :list[int] = [(idx) for idx,line  in enumerate(lines) if keyword_to_visualize.lower() in str(line).lower() ]
         
        # Create an empty multi-diimensional array using NUMPY.   
        n_lines :int =  nodes* len(visualization_str_items) + 1
        arr_size :tuple = ( n_lines ,3 )

        rP : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
        rx : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
        ry : list[list[float], list[float], list[float]]= np.empty(shape = arr_size)
        rz : list[list[float], list[float], list[float]]= np.empty(shape = arr_size) 
        
        # &________________________  Assigning data to the vectors of nodal coordinates  ________________________& 
        try:           
            # /* If the user doesn't obey the data format at the beginning, it will throw an error immediately.
            if (visualization_str_items[0] == 0):
                
                # /* Will modify the "lines" by removing the string keywords. Only coordinate values will reamin.
                del_count :int = 0
                for idx in visualization_str_items:
                    pointer = idx - del_count
                    del lines[pointer]
                    del_count +=1
                
                # /* Read .csv file column by column
                row_count :int = 0; 
                
                # /* Reading row by row for better allocation to the variables. 
                # To read column by column, use *-operator[] to unpack the arguments out of a list or tuple. 
                # !* The followwing returns as a tuple, "," is required to extract the first element only.
                for row, in zip( [ line for line in lines ] ):
                    
                    rP[ row_count,: ] = row[ 0:3 ]
                    rx[ row_count,: ] = row[ 3:6 ]
                    ry[ row_count,: ] = row[ 6:9 ]
                    rz[ row_count,: ] = row[ 9:12 ]
                    
                    
                    row_count +=1                
                
        except ValueError as err:
            print(f'%s ERROR in reading input data file. %s', err)
            
    return rP, rx, ry, rz, visualization_str_items

if __name__ == '__main__':
    raise Exception("Running this script as a standalone module is not allowed.")