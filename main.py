# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel_sans_classe import init_mat, update_mat
import time

import matplotlib.pyplot as plt

# constantes
h, w, d = 30,30,30
n = 1 # taille du cristal initial
Nc = 5000 # nombre de cristaux à générer

""" # initialisation de la matrice de fluide avec un cristal au milieu
T = init_mat(h, w, d, n)
start = time.time()
for _ in range(Nc):
    update_mat(T)
end = time.time()
print(f"Temps moyen pour la mise à jour : {(end - start)/Nc} secondes") """

# Fonction de mise à jour de la matrice de voxels
def update(i):
    for _ in range(10):
        update_mat(T)
    return T

max_frames = 200

def update_with_stop(_, i):
    if i >= max_frames:
        plt.pause(30)
        return T  # Return the final state without further updates
    return update(i)

# Génération de l'animation
a3d.generate_animation(T, lambda m,i : update(i), interval=500)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)

