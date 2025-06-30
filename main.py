
# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel import init_mat, conv, update_mat


# constantes
h, w, d = 20,20,20
n = 5 # taille du cristal initial
Nc = 100 # nombre de cristaux à générer


# initialisation de la matrice de fluide avec un cristal au milieu
T = init_mat(h, w, d, n)

# Fonction de mise à jour de la matrice de voxels
def update():
    update_mat(T)
    return conv(T)

# Génération de l'animation
a3d.generate_animation(conv(T), lambda m,i : update(), interval=500)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)