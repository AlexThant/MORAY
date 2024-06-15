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

plt.rcParams['figure.figsize']=[12,8]
plt.rcParams.update({'font.size': 12})
#

# Take the file as inputgi
file = sys.argv[1]
with open(file, "r") as f:
    csv_file = csv.reader(file, delimiter="\t")
    coord = list(csv_file)