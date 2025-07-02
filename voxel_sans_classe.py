import numpy as np
import random as rd 

def init_mat (h,w,d,n):
    
    T=np.zeros((h,w,d), dtype=bool)
             
    s=h//2-n//2
    f=w//2-n//2
    r=d//2-n//2
    
    T[s:s+n, f:f+n, r:r+n] = True

    return T

def update_mat (T):
    
    # au dessus
    T2 = np.roll(T, 1, 0)
    T2[0, :, :] = True  # un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_dessus = np.argwhere(T & (~T2))  # 1 si le voxel a un voisin libre au dessus de lui 
    v = np.array([-1, 0, 0])
    coords_libre_dessus += v

    # en dessous
    T2 = np.roll(T, -1, 0)
    T2[-1, :, :] = True
    coords_libre_dessous = np.argwhere(T & (~T2))
    v = np.array([1, 0, 0])
    coords_libre_dessous += v

    # à gauche
    T2 = np.roll(T, 1, 1)
    T2[:, 0, :] = True
    coords_libre_gauche = np.argwhere(T & (~T2))
    v = np.array([0, -1, 0])
    coords_libre_gauche += v

    # à droite
    T2 = np.roll(T, -1, 1)
    T2[:, -1, :] = True
    coords_libre_droite = np.argwhere(T & (~T2))
    v = np.array([0, 1, 0])
    coords_libre_droite += v

    # devant
    T2 = np.roll(T, 1, 2)
    T2[:, :, 0] = True
    coords_libre_devant = np.argwhere(T & (~T2))
    v = np.array([0, 0, -1])
    coords_libre_devant += v

    # derrière
    T2 = np.roll(T, -1, 2)
    T2[:, :, -1] = True
    coords_libre_derriere = np.argwhere(T & (~T2))
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

    if L.shape[0] > 0:
        idx = np.random.randint(L.shape[0])
        nv = L[idx, :]
        T[nv[0], nv[1], nv[2]] = True