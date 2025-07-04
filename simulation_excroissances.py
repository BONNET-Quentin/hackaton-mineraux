import numpy as np
import random as rd

def init_mat(h,w,d,initializers, init_pos):
    """
    Initialise une matrice 3D de taille (h, w, d) avec un cristal de taille n au centre.
    
    Parameters:
        h (int): Hauteur de la matrice.
        w (int): Largeur de la matrice.
        d (int): Profondeur de la matrice.
        initializers (list(np.3darray)): Liste de cristaux initiaux (tableaux 3D d'entiers, un entier représente une direction de croissance).
        init_pos (list(np.array)): Liste de positions initiales pour chaque cristal. Les 
                                   listes initializers et init_pos doivent être de même
                                   longueur et la position des cristaux doit être
                                   cohérente avec leur forme et la taille de la matrice.
                                   La position indiquée est celle se trouvant en haut à gauche et derrière de l'initialiseur
    Returns:
        int np.ndarray: Matrice 3D (h x w x d) initialisée avec les cristaux de initializers
    """
    T = np.zeros((h, w, d), dtype=np.uint8)
    
    for i in range(len(initializers)):
        # Get the shape of the initializer
        s = initializers[i].shape
        # Place the initializer crystal into the main matrix at the specified position
        T[
            init_pos[i][0]:init_pos[i][0]+s[0],
            init_pos[i][1]:init_pos[i][1]+s[1],
            init_pos[i][2]:init_pos[i][2]+s[2]
        ] = initializers[i]

    return T


def update_mat(T, f, f_param):
    """
    Met à jour la matrice T en faisant pousser certains cristaux

    Parameters :
        - T (uint8 np.3darray) : matrice représentant les cristaux
        - f(T, L, orientations, f_param) : fonction mettant à jour la matrice T en faisant pousser des cristaux. 
                                  L représente la liste des lieux où ils peuvent pousser et orientations leur orientation
        - f_param : un paramètre supplémentaire à donner à f
    """
    # au dessus
    Tt = np.roll(T, 1, 0)
    Tt[[0, -1], :, :] = 1; Tt[:, [0, -1], :] = 1; Tt[:, :, [0, -1]] = 1 #padding
    coords_libre_dessus = np.argwhere((T > 0) & (Tt == 0))  # 1 si le voxel a un voisin libre au dessus de lui 
    orientations_dessus = T[tuple(coords_libre_dessus.T)]
    v = np.array([-1, 0, 0])
    coords_libre_dessus += v

    # en dessous
    Tbo = np.roll(T, -1, 0)
    Tbo[[0, -1], :, :] = 1; Tbo[:, [0, -1], :] = 1; Tbo[:, :, [0, -1]] = 1
    coords_libre_dessous = np.argwhere((T > 0) & (Tbo == 0))
    orientations_dessous = T[tuple(coords_libre_dessous.T)]
    v = np.array([1, 0, 0])
    coords_libre_dessous += v

    # à gauche
    Tl = np.roll(T, 1, 1)
    Tl[[0, -1], :, :] = 1; Tl[:, [0, -1], :] = 1; Tl[:, :, [0, -1]] = 1
    coords_libre_gauche = np.argwhere((T > 0) & (Tl == 0))
    orientations_gauche = T[tuple(coords_libre_gauche.T)]
    v = np.array([0, -1, 0])
    coords_libre_gauche += v

    # à droite
    Tr = np.roll(T, -1, 1)
    Tr[[0, -1], :, :] = 1; Tr[:, [0, -1], :] = 1; Tr[:, :, [0, -1]] = 1
    coords_libre_droite = np.argwhere((T > 0) & (Tr == 0))
    orientations_droite = T[tuple(coords_libre_droite.T)]
    v = np.array([0, 1, 0])
    coords_libre_droite += v

    # devant
    Tf = np.roll(T, 1, 2)
    Tf[[0, -1], :, :] = 1; Tf[:, [0, -1], :] = 1; Tf[:, :, [0, -1]] = 1
    coords_libre_devant = np.argwhere((T > 0) & (Tf == 0))
    orientations_devant = T[tuple(coords_libre_devant.T)]
    v = np.array([0, 0, -1])
    coords_libre_devant += v

    # derrière
    Tba = np.roll(T, -1, 2)
    Tba[[0, -1], :, :] = 1; Tba[:, [0, -1], :] = 1; Tba[:, :, [0, -1]] = 1
    coords_libre_derriere = np.argwhere((T > 0) & (Tba == 0))
    orientations_derriere = T[tuple(coords_libre_derriere.T)]
    v = np.array([0, 0, 1])
    coords_libre_derriere += v

    L = np.concatenate([
        coords_libre_dessus,
        coords_libre_dessous,
        coords_libre_gauche,
        coords_libre_droite,
        coords_libre_devant,
        coords_libre_derriere
    ])

    orientations = np.concatenate([
        orientations_dessus,
        orientations_dessous,
        orientations_gauche,
        orientations_droite,
        orientations_devant,
        orientations_derriere
    ])

    f(T, L, orientations, f_param)