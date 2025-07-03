import numpy as np
import random as rd 

def init_mat (h,w,d,n):
    
    T=np.zeros((h,w,d), dtype=bool)
             
    s=h//2-n//2
    f=w//2-n//2
    r=d//2-n//2
    
    T[s:s+n, f:f+n, r:r+n] = True

    return T

def update_mat (T, C, f):
    """
    Update a matrix of boolean representing a crystal (True) in its fluid environment (False).
    
    Parameters : 
        - T : 3D boolean numpy array representing the crystal and its environment.
        - C : 3D boolean numpy array representing the voxels that were added to the crystal since its initialisation. (for display purposes only)
        - f(T, v) -> bool : Function that takes the current matrix and a voxel coordinate, and returns True if the voxel should be added to the crystal.
    """
    
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

    for i in range(L.shape[0]):
        nv = L[i,:]
        grown = f(T, nv)
        T[nv[0], nv[1], nv[2]] = grown
        C[nv[0], nv[1], nv[2]] = grown

def cristal (T, a, b, c):
    h,w,d = T.shape
    x,y,z = rd.randint(0,h-1),rd.randint(0,w-1),rd.randint(0,d-1),
    T[x,y,z] = True
   
    T[max(0,x-a//2):min(h,x+a//2), max(0,y-b//2):min(w,y+b//2), max(0,z-c//2):min(d,z+c//2)] = True
    return T

def bille(T,r):
    h,w,d = T.shape
    x,y,z = rd.randint(0,h-1),rd.randint(0,w-1),rd.randint(0,d-1),
    T[x,y,z] = True

    T[((X := np.ogrid[:h, :w, :d])[0] - x)**2 + (X[1] - y)**2 + (X[2] - z)**2 < r**2] = True  
    return T