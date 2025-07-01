import numpy as np
import random as rd 

def init_mat (h,w,d,n):
    
    T=np.zeros((h,w,d), dtype=bool)
             
    s=h//2-n//2
    f=w//2-n//2
    r=d//2-n//2
    
    T[s:s+n, f:f+n, r:r+n] = 1

    return T

def update_mat (T,L,f):
    """
    Entrée : 
    - T : tenseur d'ordre 3 de booléens indiquant si on a un cristal (True) ou du liquide (False)
    - L : ensemble de positions (set d'entiers) où un cristal peut être ajouté (liquide adjacent à un cristal). 
          La coordonnée correspondante à l'entier k est obtenue en calculant [k//n^2, (k%n^2)//n, (k%n^2)%n] avec 
    - f(v:np.array, T) : fonction renvoyant True ou False pour indiquer si un cristal doit pousser ou non
    Sortie : Met à jour T et L en ajoutant un cristal issu de l'ensemble L suivant une loi de probabilité.
    """

    