import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Example voxel array
example_matrice = np.zeros((10, 10, 10), dtype=bool)
def example_update(matrice, i) :
    if i <10 : 
        matrice[i,i,i] = True
    return matrice

def generate_animation(matrice, update, interval=500, return_fig=False, show=True):
    """
    Generate an animation from a 3D array.
    
    Parameters:
    matrice : object to call the update function on.
    update (function matrice, i -> res:np.ndarray): Function to call at each frame 
        (i : index of the frame). res is the result to display.
    interval (int): Delay between frames in milliseconds.
    frames (int): nombre d'images générées
    
    """
    (w,d,h) = matrice.shape

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type('ortho')  # Set orthographic projection
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, d)
    ax.set_zlim(0, h)

    def animate(i):
        to_display = update(matrice, i)
        ax.voxels(to_display, facecolors='cyan', alpha=0.5)

    ani = animation.FuncAnimation(fig, animate, interval=interval)

    if show:
        plt.show()
    
    if return_fig:
        return fig, ani
    return ani
    