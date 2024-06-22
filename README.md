MORAY is a mooring and riser analysis program developed in C++ and Python languages.

# To run Visualizer script, 
First, you need to generate the input data file from your ANCF FEM code.
See the example file format in the folder:: Inputs>>Beam_ANCF_coordinates.txt.

Run the script using the command below.
 python .\Main.py .\Inputs\Beam_ANCF_coordinates.txt 

 # Requirements
 #1. Python version 3.** (install via miniconda package)
 
 #2. Numpy :: to install it, simply run
 
 $conda install numpy (or)
 $python -m pip install numpy

 #3. matplotlib, to install it, simply run

 $conda install matplotlib (or ) 
 $python -m pip install matplotlib
 


 # Notes
 Define your beam's radii:: R_in and R_out in the script Main.py.
 Modifications can also be made to fit your requirements. Other modules are stored in the \src folder.


![Demo pipe deformation](Drill_pipe_demo_display.png?raw=true)
