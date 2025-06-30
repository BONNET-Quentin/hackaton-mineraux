# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# constantes
ex_h, ex_L = 50,50

# génération d'une liste de tableaux de booléens de taille (h, L) à afficher
example_matrix = np.zeros((ex_h,ex_L), dtype=bool)
example_matrices = []
for i in range(60):
    example_matrix = (1-example_matrix)  # mise à jour
    example_matrices.append(example_matrix)


def generate_animation(arrays, interval):
    """
    Generate an animation from a list of boolean arrays.
    
    Parameters:
    arrays (list): List of arrays to animate.
    interval (int): Delay between frames in milliseconds.

    """
    # génération de la figure
    fig, ax = plt.subplots()

    # génération des images à afficher
    ims = []
    for i in range(len(arrays)):
        im = ax.imshow(arrays[i], animated=True, cmap='gray', vmin=0, vmax=1)
        if i == 0:
            ax.imshow(arrays[i], cmap='gray', vmin=0, vmax=1)
        ims.append([im])

    # animation
    ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True)
    
    plt.show()