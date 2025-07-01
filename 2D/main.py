# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from animation import generate_animation, example_matrices
from classes import *
from utilities import *

# constantes
h, L = 50, 50
n = 5 # taille du cristal initial
Nc = 100 # nombre de cristaux à générer


# initialisation de la matrice de fluide avec un cristal au milieu
T = init_mat(h, L, n)
initialisation_voisins(T)

# Génération de la liste des images

ims = []
for i in range(Nc):
    generer_voxel(T)
    ims.append(conv(h, L, T))

# Génération de l'animation
generate_animation(ims, interval=50)
