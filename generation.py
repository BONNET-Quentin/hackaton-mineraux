"""
Un module pour stocker les fonctions permettant de choisir parmi une liste de voisins libres lesquels doivent pousser
"""
import numpy as np
from scipy.stats import bernoulli

NEIGHBOURS = [
    np.array([-1, 0, 0]),  # au dessus
    np.array([1, 0, 0]),   # en dessous
    np.array([0, -1, 0]),  # à gauche
    np.array([0, 1, 0]),   # à droite
    np.array([0, 0, -1]),  # devant
    np.array([0, 0, 1])    # derrière
]
MASK = np.array([0.001,0.001, 0.496, 0.496, 0.001, 0.001])*0.1 # probabilité de croissance dans chaque direction, suit le même ordre que NEIGHBOURS
p_new = lambda n : 0.0001*np.exp(-n) # probabilité de changer de direction en fonction du nombre de voisins

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
    #print(f"nombre de nouvelles orientations : {np.sum(new_crysts)}")
    new_orientations = orientations[:]
    new_orientations[new_crysts] = np.uint8(np.random.rand(np.sum(new_crysts))*255)
    """ if bernoulli.rvs(1/10):
        h, w, d = T.shape
        x,y,z = np.random.randint(0, h), np.random.randint(0, w), np.random.randint(0, d)
        T[x,y,z] = np.random.randint(1,256) """


    # Calcul du paramètre de Bernoulli pour chaque voxel pouvant croitre
    thetas = np.zeros_like(T[tuple(L.T[:3,:])], dtype=float)
    prob_masks = masks(orientations)

    for idx, pos in enumerate(tuple(L)):
        # Extraire le cube 3x3x3 autour de la position pos
        x, y, z = pos
        local_cube = T[x-1:x+2, y-1:y+2, z-1:z+2]>0
        # Produit scalaire avec le masque de probabilité correspondant
        thetas[idx] = np.sum(local_cube * prob_masks[:,:,:, idx].reshape(3,3,3))

    thetas = np.clip(thetas, 0, 1)  # S'assurer que les valeurs sont entre 0 et 1
    grown = np.bool(bernoulli.rvs(thetas)) | new_crysts

    #print(f"nombre de nouveaux cristaux : {np.sum(grown)}")
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

def def_rotation (c : int):
    "fonction injective qui a une couleur codée en [1,255] renvoie une matrice de rotation, "
    "de préférence l'espace des rotation est couvert par [1,255]"
    Rx = np.array([[1, 0, 0],
                    [0, np.cos(2*np.pi*(c-1)/255), np.sin(2*np.pi*(c-1)/255)],
                    [0, -np.sin(2*np.pi*(c-1)/255), np.cos(2*np.pi*(c-1)/255)]
                    ])
    Ry = np.array([[np.cos(20*np.pi*(c-1)/255), 0, -np.sin(20*np.pi*(c-1)/255)],
                    [0, 1, 0],
                    [np.sin(20*np.pi*(c-1)/255), 0, np.cos(20*np.pi*(c-1)/255)]
                    ])
    Rz = np.array([[np.cos(200*np.pi*(c-1)/255), np.sin(200*np.pi*(c-1)/255), 0],
                    [-np.sin(200*np.pi*(c-1)/255), np.cos(200*np.pi*(c-1)/255),0],
                    [0, 0, 1],
                    ])
    return Rx@Ry@Rz

def masks(orientations):
    """
    Retourne un tableau 3*3*3*p avec p = len(orientations) représentant les masques de 
    probabilité pour chacune des orientations de orientations
    """
    prob_masks = []
    for orientation in orientations :
        rotation = def_rotation(orientation)
        single_mask = np.einsum('ai,bj,ck,ijk->abc', rotation, rotation, rotation, mask(MASK))
        prob_masks.append(single_mask[:,:,:,np.newaxis])
    return np.concatenate(prob_masks, axis=3)

def masks_single_direction(orientations):
    return np.repeat(mask(MASK)[:, :, :, np.newaxis], orientations.shape[0], axis=3)

