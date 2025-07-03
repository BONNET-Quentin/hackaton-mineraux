# Imports
import animation3D as a3d
from simulation import init_mat, update_mat
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli
import time

# constantes
h, w, d = 50, 150, 50
n = 1 # taille du cristal initial
Nc = 5000 # nombre de cristaux à générer
NEIGHBOURS = [
    np.array([-1, 0, 0]),  # au dessus
    np.array([1, 0, 0]),   # en dessous
    np.array([0, -1, 0]),  # à gauche
    np.array([0, 1, 0]),   # à droite
    np.array([0, 0, -1]),  # devant
    np.array([0, 0, 1])    # derrière
]
def probability_function(T, v, mask):
    """
    Fonction de probabilité pour ajouter un voxel à la matrice de cristaux.
    Paramètres :
        - T : 3D boolean numpy array représentant la matrice de cristaux.
        - v : tuple de coordonnées du voxel à ajouter.
        - mask : liste de 6 probabilités, dont la somme doit être égale à 1. La
                 probabilité pour un voxel de passer de la phase liquide à la phase
                 liquide est la somme des éléments i de mask, tels que le voisin i
                 prenne la valeur True dans T. L'ordre des voisins est le même que
                 dans le tableau NEIGHBOURS.
    Retourne True si le voxel doit être ajouté, False sinon.
    
    """
    # On ne fait pas pousser le cristal sur la couche extrêmale
    if np.any(v == np.zeros(3)) or np.any(v == np.array((h-1,w-1,d-1))):
        return False 
    growth_prob = sum([T[tuple(v+NEIGHBOURS[k])] * mask[k] for k in range(6)])
    if growth_prob > 1:
        growth_prob = 1 # des erreurs de calcul peuvent faire que la somme dépasse 1
    elif growth_prob < 0:
        growth_prob = 0
    return np.bool(bernoulli.rvs(growth_prob))
MASK = [0.01,0.01, 0.48, 0.48, 0.01, 0.01]


# initialisation de la matrice de fluide avec plusieurs cristaux
T  = init_mat(h,w,d,n)
C = np.zeros((h,w,d), dtype = bool)
""" for k in range (2):
    T = cristal(T, rd.randint(5,10), rd.randint(5,10), rd.randint(5,10))
    T = bille(T,rd.randint(2,6)) """
"""
start = time.time()
for _ in range(Nc):
    update_mat(T)
end = time.time()
print(f"Temps moyen pour la mise à jour : {(end - start)/Nc} secondes") """

# Fonction de mise à jour de la matrice de voxels
def update(i):
    start = time.time()
    for _ in range(20):
        update_mat(T, C, lambda T, v: probability_function(T,v,MASK))
    print(f"Frame {i+1} générée en {(time.time() - start)} secondes")
    return T, C

# Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
max_frames = 200
def update_with_stop(_, i):
    if i >= max_frames:
        plt.pause(30)
        return T  # Return the final state without further updates
    return update(i)

# Génération de l'animation
ani = a3d.generate_animation(T, lambda _,i : update(i), interval=100, show=True)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)

# Enregistrement de l'animation
ani.save('animation.gif', writer='pillow', fps=5)