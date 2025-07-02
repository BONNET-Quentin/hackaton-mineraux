import numpy as np
import random as rd 

def init_mat (h,w,d,n):
    
    T=np.zeros((h,w,d), dtype=bool)
             
    s=h//2-n//2
    f=w//2-n//2
    r=d//2-n//2
    
    T[s:s+n, f:f+n, r:r+n] = 1


#au dessus 
    T2=np.roll(T,1,0)
    T2[0,:,:]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_dessus = np.argwhere(T & (~T2))##1 si le voxel a un voisin libre au dessus de lui
    v = np.array([-1,0,0])
    coords_libre_dessus += v
    
    #en dessous
    T2=np.roll(T,-1,0)
    T2[-1,:,:]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_dessous = np.argwhere(T & (~T2))
    v = np.array([1,0,0])
    coords_libre_dessous += v
    
    #à gauche
    T2=np.roll(T,1,1)
    T2[:,0,:]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_gauche = np.argwhere(T & (~T2)) ##1 si le voxel a un voisin libre au dessus de lui
    v = np.array([0,-1,0])
    coords_libre_gauche += v

    #à droite
    T2=np.roll(T,-1,1)
    T2[:,-1,:]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_droite = np.argwhere(T & (~T2)) ##1 si le voxel a un voisin libre au dessus de lui
    v = np.array([0,1,0])
    coords_libre_droite += v
    
    #devant
    T2=np.roll(T,1,2)
    T2[:,:,0]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_devant = np.argwhere(T & (~T2)) ##1 si le voxel a un voisin libre au dessus de lui
    v = np.array([0,0,-1])
    coords_libre_devant += v
    
    #derrière
    T2=np.roll(T,-1,2)
    T2[:,:,-1]=1  ##un voxel tout en haut ne peut pas avoir de voisins au dessus
    coords_libre_derriere = np.argwhere(T & (~T2)) ##1 si le voxel a un voisin libre au dessus de lui
    v = np.array([0,0,1])
    coords_libre_derriere += v
    
    L=bijection(np.concatenate([coords_libre_dessus,
                      coords_libre_dessous,
                      coords_libre_gauche,
                      coords_libre_droite,
                      coords_libre_devant,
                      coords_libre_derriere]))
    
    L=set(L)
    
    return T, L

def update_mat (T,L):
    """
    Entrée : 
    - T : tenseur d'ordre 3 représentant la phase présente en chaque coordonnée
    - L : set(np.array) contenant les coordonnées des voxels qui peuvent pousser (liquide, adjacent à un solide)

    Sortie : Met à jour T et L en faisant pousser un cristal parmi les éléments de L
    """
    
    if L != {}:

        idx=np.random.randint(len(L))
        nv=L[idx]

        T[nv[0],nv[1],nv[2]]=1
        L.pop(nv)
    



def bijection(t,n):
    '''
    permet de passer d'un array de coordonnées en son entier 
    '''
    return t[:,0]*n**2 + t[:,1]*n + t[:,2] 
    
