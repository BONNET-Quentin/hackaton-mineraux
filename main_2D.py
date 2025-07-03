# Imports
from animation2D import generate_animation
from simulation import init_mat, update_mat, cristal, bille
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli


# constantes
h, w, d = 50, 150, 50
n = 1 # taille du cristal initial


# initialisation de la matrice de fluide avec un cristal au milieu
T  = init_mat(h,w,d,n)
C = np.zeros((h,w,d), dtype = bool)
""" for k in range (2):
    T = cristal(T, rd.randint(5,10), rd.randint(5,10), rd.randint(5,10))
    T = bille(T,rd.randint(2,6)) """

NEIGHBOURS = [
    np.array([-1, 0, 0]),  # au dessus
    np.array([1, 0, 0]),   # en dessous
    np.array([0, -1, 0]),  # à gauche
    np.array([0, 1, 0]),   # à droite
    np.array([0, 0, -1]),  # devant
    np.array([0, 0, 1])    # derrière
]
def probability_function(T, C, L, mask):
    """
    Fonction de probabilité pour ajouter un voxel à la matrice de cristaux.
    Paramètres :
        - T, C : 3D boolean numpy array représentant la matrice de cristaux. (+ affichage)
        - L : matrice de coordonnées des voxels à pouvant être ajoutés (3 lignes).
        - mask : liste de 6 probabilités, dont la somme doit être égale à 1. La
                 probabilité pour un voxel de passer de la phase liquide à la phase
                 liquide est la somme des éléments i de mask, tels que le voisin i
                 prenne la valeur True dans T. L'ordre des voisins est le même que
                 dans le tableau NEIGHBOURS.
    Met à jour les matrices T et C en faisant pousser certains cristaux de la liste donnée par L.

    """
    """ # On ne fait pas pousser le cristal sur la couche extrêmale
    if np.any(v == np.zeros(3)) or np.any(v == np.array((h-1,w-1,d-1))):
        return False 
    growth_prob = sum([T[tuple(v+NEIGHBOURS[k])] * mask[k] for k in range(6)])
    if growth_prob > 1:
        growth_prob = 1 # des erreurs de calcul peuvent faire que la somme dépasse 1
    elif growth_prob < 0:
        growth_prob = 0
    return np.bool(bernoulli.rvs(growth_prob)) """
    # Calcul du paramètre de Bernoulli pour chaque voxel pouvant croitre
    thetas = np.zeros_like(T[tuple(L.T)], dtype=float)
    for i in range(6):
        thetas += T[tuple((L + NEIGHBOURS[i]).T)] * mask[i]
    thetas = np.clip(thetas, 0, 1)  # S'assurer que les valeurs sont entre 0 et 1
    grown = np.bool(bernoulli.rvs(thetas))
    print(f"nombre de nouveaux cristaux : {np.sum(grown)}")
    # Mise à jour des matrices T et C
    T[tuple(L.T)] = grown
    C[tuple(L.T)] = grown 

    
MASK = np.array([0.01,0.01, 0.48, 0.48, 0.01, 0.01])

# Fonction de mise à jour de la matrice de voxels
def update(i):
    global T, C
    for _ in range(1):
        update_mat(T, C, lambda T,C,L : probability_function(T, C, L, MASK))
    print(f"Frame {i} générée")
    return T, C

# Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
max_frames = 100
def update_with_stop(_, i):
    global T, C
    if i >= max_frames:
        return T, C  # Return the final state without further updates
    return update(i)

# Génération de l'animation 2D et de l'image 3D côte à côte

ims = []
for i in range(max_frames + 1):
    # Mise à jour de la matrice et récupération des données à afficher
    T, C = update_with_stop(None, i)
    ims.append([T.copy(), C.copy()])  # Append both matrices

print("Calcul 2D terminé")
direction = np.random.randint(0, 2)  # Direction aléatoire pour l'animation 2D
plan = np.random.randint(0, d)  # Plan aléatoire pour l'animation 2D selon la direction

# Création d'une figure avec deux sous-graphes côte à côte
fig = plt.figure(figsize=(16, 6))

# Sous-graphe pour l'animation 2D
ax1 = fig.add_subplot(1, 2, 1)
print("Animation 2D en cours de génération...")
ani = generate_animation(ims, direction, plan, interval=500, fig=fig, ax=ax1)

# Sous-graphe pour l'image 3D
print("Image 3D en cours de génération...")
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.set_proj_type('ortho')
ax2.set_box_aspect([h, w, d])
ax2.set_xlim(0, h)
ax2.set_ylim(0, w)
ax2.set_zlim(0, d)

to_display, growth_to_display = T, C
valeur = plan  # Valeur du plan à afficher
plan_mask = np.zeros((h, w, d), dtype=bool)
# Création du plan à afficher selon la direction
if direction == 0:  # Plan x
    plan_mask[valeur, :, :] = True
elif direction == 1:  # Plan y
    plan_mask[:, valeur, :] = True
else:  # Plan z
    plan_mask[:, :, valeur] = True
ax2.voxels(to_display.astype(bool), facecolors='cyan', alpha=0.5)
ax2.voxels(growth_to_display.astype(bool), facecolors='red', alpha=0.5)
ax2.voxels(plan_mask, facecolors='yellow', alpha=0.5)  # Plan en jaune

plt.tight_layout()
plt.show()