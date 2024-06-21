# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
#                   Created on Thu Jun 20 19:56:30 2024                       #
#                          @author: Thant Zin Htun                            #
#                        tzhtun@naoe.eng.osaka-u.ac.jp                        #
#                       -*- ANCF Beam's visualizer -*-                        #
#               -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-              #
# -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -*-  -#
import numpy as np
import matplotlib; matplotlib.get_backend(); matplotlib.use('TkAgg')  # for compatibility on Mac OS
import matplotlib.pyplot as plt             # for generating plots & graphs
import matplotlib.cm as cm
from matplotlib.colors import Normalize

plt.rcParams['figure.figsize']=[20,15]
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams.update({'font.size': 12})
fig :object = plt.figure()
ax :object  = fig.add_subplot(111, projection= '3d')


class DISPLAY:
    
    def __init__(self) -> None:
        pass
    
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def show_colormap_deformation(self, X :list[float,], Y :list[float,], Z :list[float]):
        """_summary_
        Choose a variable to show contour color on a 3D base plot.

        Args:
            colormap_variable (str, optional): _description_. Defaults to 'Transverse Deformation'.
            variable can be either of "Deformation, Von-misses stresses, Green-Lagrange strains".
        """
        # If colormap variable is defined, 
        hori_displacement =  X**2 + Y**2
        norm = Normalize(vmin = np.nanmin(hori_displacement), vmax= np.nanmax(hori_displacement))
        col_map= cm.rainbow
        face_col = col_map(norm(hori_displacement))
        col_variable = face_col
            
        surf = ax.plot_surface(X, Y, Z, 
                            facecolors= col_variable, cmap='rainbow',
                            rstride=1, cstride=1, 
                            linestyle= 'dashed',
                            linewidth= 0.25, alpha= 0.9, antialiased= True, 
                            zorder=2
                            ) # rstride=1, cstride=1, cmap=cm.winter, linewidth=0.5, antialiased=True, zorder = 0.5)
        
        
        return surf
    
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def pyplot_3d_surface(self, X :list[float,], Y :list[float,], Z :list[float], 
                          Xcrs_t :list[float], Ycrs_t: list[float], Zcrs_t: list[float], 
                          Xcrs_b: list[float], Ycrs_b: list[float], Zcrs_b: list[float], 
                          X_in :list[float] = [None,], Y_in: list[float] = [None,], 
                          plot_id : int= 0, setting_flag: list[bool, bool] = [False, False], 
                          colormap_variable :str = 'deformation'
                          ) -> None:
        """Generate a 3D surface plot using matplotlib. 
           A customized variable to show colormap can be set too. 

        """
            
        # Plot the surface
        alpha_val, f_color, ls = ((0., 'k', 'dashed') if plot_id == 0 else
                                  (0, 'w', 'solid')
                            ) 
        
        surf = ax.plot_surface(X, Y, Z, 
                            color=f_color, edgecolors = 'k',
                            rstride=1, cstride=1, 
                            linestyle= ls,
                            linewidth= 0.25, alpha= alpha_val, antialiased= True, 
                            zorder=2
                            ) # rstride=1, cstride=1, cmap=cm.winter, linewidth=0.5, antialiased=True, zorder = 0.5)

        if X_in.any() != None:
            surf_1 = ax.plot_surface(X_in, Y_in, Z, 
                                    color='k', edgecolors = 'k',
                                    rstride=1, cstride=1, 
                                    linestyle= ls,
                                    linewidth= 0.25, alpha= alpha_val, antialiased= True, 
                                    zorder=1
                                    )
        #___ End caps ___  
        edge_col :str = ('k' if setting_flag[1] else
                         None
                         )
            
        ax.plot_surface(Xcrs_t, Ycrs_t, Zcrs_t, 
                        edgecolors = edge_col, 
                        alpha= 1.0, 
                        linewidth = 1, linestyle= 'solid',
                        antialiased= True, 
                        zorder=0
                        )
        
        ax.plot_surface(Xcrs_b, Ycrs_b, Zcrs_b, 
                        edgecolors = edge_col,
                        alpha= 1.0, 
                        linewidth = 1, linestyle= 'solid',
                        antialiased= True, 
                        zorder=0
                        )
        
        
        # Add colormap plot for a defined variable
        if (plot_id !=0 and str(colormap_variable).lower() == 'deformation'):
            surf_colormap = self.show_colormap_deformation(X,Y, Z)
            return surf_colormap
        else:
            return surf
        
        
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__* 
    def pyplot_settings_helper(self, surf, title: str = None, background_trans: bool = True, colorbar_label :str= 'Normalized deformation [m]',shrink_color_bar: bool = True)-> None: #fig: object, surf: object,
        # Make legend, set axes limits and labels
        #ax.legend("Legend")
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.5, 0.5)
        ax.set_zlim(-3, 0.5)
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')

        # Customize the view angle so it's easier to see the figure
        # Default view angle (elev=28., azim=45, roll=0)
        ax.view_init(elev=20., azim=-45, roll=0)
        # set viewing angle
        ax.dist = 5    # zoom (define perspective)

        if not title is None: ax.set_title(title)
        ax.set_aspect('equal')

        #ax.set(xticklabels=[],
        #   yticklabels=[],
        #   zticklabels=[])
        #ax.set_box_aspect([1.0, 1.0, 1.0])

        if background_trans:
            # make the panes transparent
            ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            # make the grid lines transparent
            ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
            ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
            ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
       
       
       # Adding the colorbar
        cbaxes = fig.add_axes([0.7, 0.3, 0.01, 0.5]) 
        if shrink_color_bar:
            cbar = fig.colorbar(surf, shrink=0.5, aspect=5, orientation='vertical', cax=cbaxes)
        else:
            cbar = fig.colorbar(surf, orientation='vertical', cax= cbaxes)
        
        
        cbar.solids.set_edgecolor("face")
        cbar.set_label(colorbar_label)
        
        # Show the plot with customized tight layout
        #fig.tight_layout(rect=[0, 0.03, 1, 1])

        return None
        
        
        
     # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    @staticmethod
    def show_fig():
        return plt.show()
    
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    @staticmethod
    def save_fig(filename : str= 'figure', dpi_value: int= 600):
        """Set the file name and resolution via dpi_value (max is 1200, default value is 600 dpi.)

        Args:
            filename (str, optional): _description_. Defaults to 'figure'.
            dpi_value (int, optional): _description_. Defaults to 600.

        Returns:
            _type_: _description_
        """
        return plt.savefig(filename, format='png', dpi=dpi_value, bbox_inches='tight')
        
    # __*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*__*
    def mayavi_3d_surface(X, Y, Z, Xcrs_t, Ycrs_t, Zcrs_t, Xcrs_b, Ycrs_b, Zcrs_b,  X_in :list[float] = [None,], Y_in: list[float] = [None,]) -> None:
        from mayavi import mlab
        
        title :str = '3D Parametric Surface:'
        purple = (0.5,0,1)
        representation_style :str = 'surface'
        #mlab.surf(Z, warp_scale='auto')
        mlab.clf()
        fig = mlab.mesh(X,Y,Z, representation= representation_style, color= purple)
        mlab.mesh(Xcrs_t, Ycrs_t, Zcrs_t, representation= representation_style, color= purple)
        mlab.mesh(Xcrs_b, Ycrs_b, Zcrs_b, representation= representation_style, color= purple)
        if X_in.all() != None: 
            fig_1 = mlab.mesh(X_in,Y_in,Z, representation= representation_style, color= purple)
        mlab.axes(
                    xlabel='x', ylabel='z', zlabel=title,
                    x_axis_visibility=True, y_axis_visibility=True, z_axis_visibility=True
                    )
        
        mlab.orientation_axes(xlabel='x', ylabel='z', zlabel=title)
        mlab.title(title)    
        #mlab.figure(figure=fig, bgcolor=(0, 0, 0), fgcolor=(0.5, 0.5, 0.5)); 
        #mlab.outline()
        
        #mlab.figure(figure=fig_1, bgcolor=(0, 0, 0), fgcolor=(0.5, 0.5, 0.5))
        mlab.show()
        
        return None

# Object lists
DISPLAY = DISPLAY()

if __name__ == '__main__':
    raise Exception("Running this script as a standalone module is not allowed.")
    