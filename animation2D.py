# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as clrs

def generate_animation(T, ims, direction, plan, interval, fig=None, ax=None):
    """
    Génère une animation à partir d'une liste d'éléments [T, C], où T et C sont des tableaux 3D.
    Affiche T en bleu et C en rouge sur le même plan z.
    """
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    h, L, D = ims[0].shape
    variable = 'x' if direction == 0 else 'y' if direction == 1 else 'z'
    abscisse = L if direction == 0 else D if direction == 1 else h
    ordonnée = D if direction == 0 else h if direction == 1 else L
    taille = h if direction == 0 else L if direction == 1 else D

    ax.set_title(f'Plan de {variable} = {plan} sur {taille} pour 2D')  # titre avec le plan
    frames = []
    ax.set_facecolor('white')

    for T in ims:
        if direction == 0:  # Plan x
            slice_T = T[plan, :, :]
        elif direction == 1:  # Plan y
            slice_T = T[:, plan, :]
        else:  # Plan z
            slice_T = T[:, :, plan]
    

        # Bleu pour T
        base_cmap = plt.get_cmap('tab20', 20) # on sélectionne les 20 couleurs de la table 'tab20'
        colors = [base_cmap(i%20) for i in range (256)] # on récupère nos 256 couleurs (répétition des 20 couleurs)
        cmap = clrs.ListedColormap(colors)
        rgba_colors = cmap(slice_T)
        rgba_colors[slice_T == 0] = [0, 0, 0, 0] # on rend transparent le fluide qui a une valeur de 0


        im = ax.imshow(rgba_colors, animated=True, vmin=0, vmax=1)
        frames.append([im])

    ani = animation.ArtistAnimation(fig, frames, interval=interval, blit=True)
    return ani
