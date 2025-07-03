# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def generate_animation(ims, direction, plan, interval, fig=None, ax=None):
    """
    Génère une animation à partir d'une liste d'éléments [T, C], où T et C sont des tableaux 3D.
    Affiche T en bleu et C en rouge sur le même plan z.
    """
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    h, L, D = ims[0][0].shape
    variable = 'x' if direction == 0 else 'y' if direction == 1 else 'z'
    abscisse = L if direction == 0 else D if direction == 1 else h
    ordonnée = D if direction == 0 else h if direction == 1 else L
    taille = h if direction == 0 else L if direction == 1 else D

    ax.set_title(f'Plan de {variable} = {plan} sur {taille} pour 2D')  # titre avec le plan
    frames = []
    ax.set_facecolor('white')

    for T, C in ims:
        img = np.zeros((abscisse, ordonnée, 3), dtype=np.float32)
        if direction == 0:  # Plan x
            slice_T = T[plan, :, :]
            slice_C = C[plan, :, :]
        elif direction == 1:  # Plan y
            slice_T = T[:, plan, :]
            slice_C = C[:, plan, :]
        else:  # Plan z
            slice_T = T[:, :, plan]
            slice_C = C[:, :, plan]
            
        # Appliquer une couleur avec transparence (alpha) similaire à l'animation 3D
        # Bleu semi-transparent pour T, rouge semi-transparent pour C, fond blanc
        alpha_T = 0.4
        alpha_C = 0.4
        img[:, :, :] = 1  # fond blanc

        # Bleu pour T
        mask_T = (slice_T == 1)
        img[mask_T] = (1 - alpha_T) * img[mask_T] + alpha_T * np.array([0, 0, 1])

        # Rouge pour C (prioritaire si superposé)
        mask_C = (slice_C == 1)
        img[mask_C] = (1 - alpha_C) * img[mask_C] + alpha_C * np.array([1, 0, 0])

        im = ax.imshow(img, animated=True, vmin=0, vmax=1)
        frames.append([im])

    ani = animation.ArtistAnimation(fig, frames, interval=interval, blit=True)
    return ani
