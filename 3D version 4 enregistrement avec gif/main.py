# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel import init_mat, conv, update_mat

import matplotlib.pyplot as plt
from matplotlib import animation

# constantes
h, w, d = 30,30,30
n = 1

# initialisation de la matrice
T = init_mat(h, w, d, n)

# Fonction de mise à jour
def update(i):
    for _ in range(10):
        update_mat(T)
    print(f"Frame {i}")
    return conv(T)

max_frames = 100

def update_with_stop(_, i):
    if i >= max_frames:
        plt.pause(30)
        return conv(T)  # Return the final state without further updates
    return update(i)

# Génération de l'animation
fig, ani = a3d.generate_animation(conv(T), update_with_stop, interval=100, return_fig=True)

# Enregistrement de l'animation
# PRECISION : il faut fermer la fenetre et laisser continuer à générer les frames jusqu'à stopper avec CTRL C
ani.save("animation.gif", writer='pillow', fps=100)
