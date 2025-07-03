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

def generate_animation(matrice, update, interval=500, show=True):
    """
    Generate an animation from a 3D array.
    
    Parameters:
    matrice : object to call the update function on.
    update (function matrice, i -> T:np.ndarray, C): Function to call at each frame 
        (i : index of the frame). T is the whole matrix to display and C represents the crystals that were added since the intialisation.
    interval (int): Delay between frames in milliseconds.
    show (bool): If True, display the animation in time. If False, does not display it. (default : True)

    Returns the animation object that can then be used to save the animation.
    """
    (h,w,d) = matrice.shape

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_proj_type('ortho')  # Set orthographic projection
    ax.set_box_aspect([h, w, d])
    ax.set_xlim(0, h)
    ax.set_ylim(0, w)
    ax.set_zlim(0, d)
    
    base_cmap = plt.get_cmap('tab20', 20) # on sélectionne les 20 couleurs de la table 'tab20'
    colors = [base_cmap[i%20] for i in range (255)] # on récupère nos 256 couleurs (répétition des 20 couleurs)
    cmap = plt.ListedColormap(colors)
    
    def animate(i):
        
        to_display = update(matrice, i)
        rgba_colors = cmap(to_display) 
        rgba_colors[to_display == 0] = [0, 0, 0, 0] # on rend transparent le fluide qui a une valeur de 0
        
        ax.voxels(to_display, facecolors=rgba_colors, alpha=0.5)

    ani = animation.FuncAnimation(fig, animate, interval=interval)

    if show:
        plt.show()
    
    return ani
    