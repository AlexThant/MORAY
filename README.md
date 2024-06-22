MORAY is a mooring and riser analysis program developed in C++ and Python languages.

# To run Visualizer script, 
>[!IMPORTANT]
><p>First, absolute nodal coordinates for a global position vector and a complete set of three position gradient vectors need to be generated from ANCF FEM code.<br>
>See the example file format in the folder:: Inputs>>Beam_ANCF_coordinates.txt.</p>

<p>Run the script using the command below.</p>
<code>$ python .\Main.py .\Inputs\Beam_ANCF_coordinates.txt</code>

 # Requirements
 >[!TIP]
 > - 1. <p> Python version 3.** (install via *[miniconda package](https://docs.anaconda.com/miniconda/)*).<br>
 > - 2. Numpy :: to install it, simply run<br><br>
 ><code>$ conda install numpy</code>(or)<br>
 ><code>$ python -m pip install numpy</code><br><br>
 > - 3. matplotlib :: to install it, simply run<br><br>
 ><code>$ conda install matplotlib</code> (or)<br> 
 ><code>$ python -m pip install matplotlib</code><br><br>
 > - 4. To use *[Mayavi](https://mayavi.readthedocs.io/en/latest/)*, install *[PyQt5](https://pypi.org/project/PyQt5/)* and *[Mayavi](https://mayavi.readthedocs.io/en/latest/)* modules.<br><br>
><code>$ python -m pip install pyqt5</code><br>
><code>$ python -m pip install mayavi</code></p>

 >[!NOTE]
 >Define your beam's radii:: R_in and R_out in the script Main.py.
 >Modifications can also be made to fit your requirements. Other modules are stored in the *[\src](https://github.com/AlexThant/MORAY/blob/Visualizer/Visualizer/src)* folder.)


![Demo pipe deformation](https://github.com/AlexThant/MORAY/blob/Visualizer/Visualizer/Drill_pipe_demo_display.png)
![Demo pipe deformation in Mayavi](https://github.com/AlexThant/MORAY/blob/Visualizer/ANCF_pipe_snapshot.png)


# Citation
To cite MORAY Visualizer in public use:
${\color{lightgreen}TZ\space Htun\space (2024)\space::\space \textrm{MORAY}, \space \textrm{url}::}$ https://github.com/AlexThant/MORAY/tree/Visualizer.

