
# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel import init_mat, conv, update_mat, free_voxels, get_etat
import time
import matplotlib.pyplot as plt
import numpy as np


# constantes
h, w, d = 30,30,30
n = 1 # taille du cristal initial
Nc = 100 # nombre de cristaux à générer
Nc = 100 # nombre de cristaux à générer


# initialisation de la matrice de fluide avec un cristal au milieu
T = init_mat(h, w, d, n)

# Fonction de mise à jour de la matrice de voxels()
count = 5000
start = time.time()
for _ in range(count):
    get_etat(T)
end = time.time()
print("temps moyen pour extraire les états : ", (end-start)/count)



""" def update(i):
    start = time.time()
    for k in range(10*(i**3)):
        update_mat(T)
    sim_num.append(10*(i**3))
    durations.append(time.time()-start)
    return conv(T) """

# Génération de l'animation
# a3d.generate_animation(conv(T), lambda m,i : update(i), interval=500)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)

