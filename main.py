# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel_sans_classe import init_mat, update_mat, cristal, bille
import random as rd
import time
import numpy as np

import matplotlib.pyplot as plt

# constantes
h, w, d = 50, 50, 50
n = 1 # taille du cristal initial
Nc = 5000 # nombre de cristaux à générer

# initialisation de la matrice de fluide avec un cristal au milieu
T  = init_mat(h,w,d, 1)
C = np.zeros((h,w,d), dtype = bool)
for k in range (2):
    T = cristal(T, rd.randint(5,10), rd.randint(5,10), rd.randint(5,10))
    T = bille(T,rd.randint(2,6))
"""
start = time.time()
for _ in range(Nc):
    update_mat(T)
end = time.time()
print(f"Temps moyen pour la mise à jour : {(end - start)/Nc} secondes") """

# Fonction de mise à jour de la matrice de voxels
def update(i):
    for _ in range(10*(i**2)):
        update_mat(T, C)
    print(f"Frame {i} générée")
    return T, C

# Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
max_frames = 200
def update_with_stop(_, i):
    if i >= max_frames:
        plt.pause(30)
        return T  # Return the final state without further updates
    return update(i)

# Génération de l'animation
fig, ani = a3d.generate_animation(T, C, lambda m,i : update(i), interval=100, return_fig=True, show=False)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)

# Enregistrement de l'animation
ani.save('animation.gif', writer='pillow', fps=5)