# Imports
import animation3Dexcroisssance as a3de
from simulation_excroissances import init_mat, update_mat
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli
import time

# constantes
h, w, d = 200, 500, 200
NEIGHBOURS = [
    np.array([-1, 0, 0]),  # au dessus
    np.array([1, 0, 0]),   # en dessous
    np.array([0, -1, 0]),  # à gauche
    np.array([0, 1, 0]),   # à droite
    np.array([0, 0, -1]),  # devant
    np.array([0, 0, 1])    # derrière
]
MASK = np.array([0.002,0.002, 0.496, 0.496, 0.002, 0.002]) # probabilité de croissance dans chaque direction, suit le même ordre que NEIGHBOURS

# fonction déterminant si on doit générer ou non un cristal
def generation(T, L, orientations, masks, p_new):
    """Ajoute aléatoirement des cristaux à la matrice T. /!\ Il doit toujours rester un espace libre autour de chaque candidat /!\
    
    Paramètres :
        - T : matrice à modifier
        - L : 3*p array représentant les coordonnées ou un cristal peut pousser
        - orientations : 1*p array représentant l'orientation (int) des cristaux en cours de croissance
        - masks(int np.array) : fonction qui à une liste d'orientations (entiers) associe une liste de
                                masques de probabilités permettant de déterminer si un cristal devrait croître ou non
                                Le format est un tableau 4D (3*3*3*p)
        - p_new(l) : Associe à une liste de nombre de voisins la liste des probabilités qu'un nouveau cristal 
                     pousse dans une direction différente en fonction du nombre de ses voisins
    """
    # Génération des nouveaux cristaux
    ps_new = p_new(np.arange(7))
    n_voisins = sum([T[tuple((L+NEIGHBOURS[i]).T)]>0 for i in range(6)])
    new_crysts = np.bool(bernoulli.rvs(ps_new[n_voisins]))
    print(f"nombre de nouvelles orientations : {np.sum(new_crysts)}")
    new_orientations = orientations[:]
    new_orientations[new_crysts] = np.uint8(np.random.rand(np.sum(new_crysts))*255)


    # Calcul du paramètre de Bernoulli pour chaque voxel pouvant croitre
    thetas = np.zeros_like(T[tuple(L.T[:3,:])], dtype=float)
    prob_masks = masks(orientations)

    for idx, pos in enumerate(tuple(L)):
        # Extraire le cube 3x3x3 autour de la position pos
        x, y, z = pos
        local_cube = T[max(x-1,0):x+2, max(y-1,0):y+2, max(z-1,0):z+2]>0
        # Produit scalaire avec le masque de probabilité correspondant
        thetas[idx] = np.sum(local_cube * prob_masks[:,:,:, idx].reshape(3,3,3))

    thetas = np.clip(thetas, 0, 1)  # S'assurer que les valeurs sont entre 0 et 1
    grown = np.bool(bernoulli.rvs(thetas)) | new_crysts

    print(f"nombre de nouveaux cristaux : {np.sum(grown)}")
    # Mise à jour de la matrice T
    T[tuple(L.T)] = grown*new_orientations

def mask(m):
    """
    Retourne un tableau 3*3*3 représentant le masque donné en entrée
    """
    t = np.zeros((3,3,3), dtype=float)
    t[1,1,1] = 1
    t[0,1,1] = m[0]
    t[2,1,1] = m[1]
    t[1,0,1] = m[2]
    t[1,2,1] = m[3]
    t[1,1,0] = m[4]
    t[1,1,2] = m[5]

    return t

from utilities import mat
def masks(orientations):
    """
    Retourne un tableau 3*3*3*p avec p = len(orientations) représentant les masques de 
    probabilité pour chacune des orientations de orientations
    """
    prob_masks = []
    for orientation in orientations :
        rotation = mat(orientation)
        single_mask = np.einsum('ijk,kl->ijl', mask(MASK),rotation)
        prob_masks.append(single_mask[:,:,:,np.newaxis])
    return np.concatenate(prob_masks, axis=3)

def masks_single_direction(orientations):
    return np.repeat(mask(MASK)[:, :, :, np.newaxis], orientations.shape[0], axis=3)

p_new = lambda n : 0.01*np.exp(-n)


# initialisation de la matrice de fluide avec plusieurs cristaux
T  = init_mat(h,w,d,[np.ones((1,1,1), dtype=np.uint8)], [np.array([h//2,w//2,d//2])])
""" for k in range (2):
    T = cristal(T, rd.randint(5,10), rd.randint(5,10), rd.randint(5,10))
    T = bille(T,rd.randint(2,6)) """
"""
start = time.time()
for _ in range(Nc):
    update_mat(T,C)
end = time.time()
print(f"Temps moyen pour la mise à jour : {(end - start)/Nc} secondes") """

# Fonction de mise à jour de la matrice de voxels
def update(i):
    start = time.time()
    for _ in range(50):
        update_mat(T, lambda T,L,orientations,_ : generation(T,L,orientations,masks, p_new), None)
    print(f"Frame {i+1} générée en {(time.time() - start)} secondes")
    return T

# Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
max_frames = 200
def update_with_stop(_, i):
    if i >= max_frames:
        plt.pause(30)
        return T  # Return the final state without further updates
    return update(i)

# Génération de l'animation
ani = a3de.generate_animation(T, update_with_stop, interval=100, show=False)

# Exemple d'animation 2D
# a3d.generate_animation(a3d.example_matrice, a3d.example_update, interval=500)

# Enregistrement de l'animation
ani.save('animation.gif', writer='pillow', fps=10)