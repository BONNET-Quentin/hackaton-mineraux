# Imports
from animation2D import generate_animation
from simulation import init_mat, update_mat, cristal, bille
import random as rd
import numpy as np
import matplotlib.pyplot as plt


# constantes
h, w, d = 50, 50, 50
n = 1 # taille du cristal initial


# initialisation de la matrice de fluide avec un cristal au milieu
T  = init_mat(h,w,d, 1)
C = np.zeros((h,w,d), dtype = bool)
for k in range (2):
    T = cristal(T, rd.randint(5,10), rd.randint(5,10), rd.randint(5,10))
    T = bille(T,rd.randint(2,6))

# Fonction de mise à jour de la matrice de voxels
def update(i):
    global T, C
    for _ in range(10*(i**2)):
        update_mat(T, C)
    print(f"Frame {i} générée")
    return T, C

# Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
max_frames = 10
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
ax2.set_box_aspect([1, 1, 1])
ax2.set_xlim(0, w)
ax2.set_ylim(0, d)
ax2.set_zlim(0, h)

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