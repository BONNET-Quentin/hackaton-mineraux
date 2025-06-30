import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Example voxel array
example_matrice = np.zeros((10, 10, 10), dtype=bool)
def example_update(matrice, i) :
    if i <10 : 
        matrice[i,i,i] = True

def generate_animation(matrice, update, interval=500):
    """
    Generate an animation from a 3D array.
    
    Parameters:
    matrice (np.ndarray): Initial 3D array.
    update (function): Function to update the 3D array.
    interval (int): Delay between frames in milliseconds.
    
    """
    (w,d,h) = matrice.shape

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, w)
    ax.set_ylim(0, d)
    ax.set_zlim(0, h)

    def animate(i):
        update(matrice, i)
        ax.voxels(matrice, facecolors='cyan', alpha=0.5)

    ani = animation.FuncAnimation(fig, animate, interval=interval)
    
    plt.show()