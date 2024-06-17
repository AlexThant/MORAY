
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Define the parametric equations for the torus
def torus(R, r, u, v):
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z
# Create a grid of the u and v values
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 2 * np.pi, 100)
u, v = np.meshgrid(u, v)
# Calculate the coordinates of the torus
R = 3 
r = 1  
x, y, z = torus(R, r, u, v)
# Plot the torus
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, color='c', edgecolor='k', alpha=0.6)
fig.colorbar(surf)
# Labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Parametric Surface: Torus')
# Show the plot
plt.show()


#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
##surf = ax.plot_surface(X1, X2, Y_plot, cmap='bwr', linewidth=0)
#fig.colorbar(surf)
#ax.set_title("Surface Plot")
#fig.show()
