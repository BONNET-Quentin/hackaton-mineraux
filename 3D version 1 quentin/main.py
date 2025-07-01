
# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from animation import generate_animation, example_matrices
from classes import *
from utilities import *
import animation3D as a3d

# constantes
h, w, d = 20,20,20
n = 5 # taille du cristal initial
Nc = 100 # nombre de cristaux à générer


# initialisation de la matrice de fluide avec un cristal au milieu
T = init_mat(h, w, d, n)
initialisation_voisins(T)

# Fonction de mise à jour de la matrice de voxels
def update():
    generer_voxel(T)
    return conv(h, w, d, T)

# Génération de l'animation
a3d.generate_animation(conv(h, w, d, T), lambda m,i : update(), interval=10)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)