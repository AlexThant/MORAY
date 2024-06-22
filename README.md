MORAY is a mooring and riser analysis program developed in C++ and Python languages.

# To run Visualizer script, 
<p>First, you need to generate the input data file from your ANCF FEM code.<br>
See the example file format in the folder:: Inputs>>Beam_ANCF_coordinates.txt.</p>

<p>Run the script using the command below.</p>
<code>python .\Main.py .\Inputs\Beam_ANCF_coordinates.txt</code> 

 # Requirements
 #1. Python version 3.** (install via miniconda package)
 
 #2. Numpy :: to install it, simply run
 
 <code>conda install numpy</code>
 (or)
 '''console
 <code>python -m pip install numpy</code>
'''
 #3. matplotlib, to install it, simply run

 <code>conda install matplotlib</code> (or ) 
 <code>python -m pip install matplotlib</code>
 


 [!Note]
 Define your beam's radii:: R_in and R_out in the script Main.py.
 Modifications can also be made to fit your requirements. Other modules are stored in the \src folder.


![Demo pipe deformation](https://github.com/AlexThant/MORAY/blob/Visualizer/Visualizer/Drill_pipe_demo_display.png)
