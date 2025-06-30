import numpy as np
import random as rd 

# Fichier pour créer les classes

class voxel :
    def __init__(self,coord,etat,voisins):
        self.coord=coord
        self.etat=etat
        self.voisins=voisins

@np.vectorize 
def get_etat(v:voxel):
    return v.etat
    
    
def init_mat (h,L,n):
    
    T=np.zeros((h,L), dtype=object)
    
    for i in range (h):      ##on définit la matrice 
            for j in range (L):
                v=voxel((i,j),0,[])
                T[i,j]=v
            
            
    s=int(h/2)-int(n/2)
    f=int(L/2)-int(n/2)
    
    for i in range (s,s+n):     ##on définit le cristal
        for j in range (f,f+n):
            T[i,j].etat=1
    
    for i in range (h) :
        for j in range (L) :
            l=[]
            if i+1<h:
                l.append(T[i+1,j])
            if j-1>0:
                l.append(T[i-1,j])
            if j+1<L:
                l.append(T[i,j+1])
            if i-1>0: 
                l.append(T[i-1,j])
            T[i,j].voisins=l
    
    return T

    
def conv (h,L,T):  ##fait un tableau affichable à partir du tableau de voxel 
    A=np.zeros((h,L))
    for i in range (h):
        for j in range (L):
            A[i,j]=get_etat(T[i,j])
    return A 

def free_voxels (T):
    M=T[get_etat(T)==1]   
    L=[]
    for m in M : 
        for v in m.voisins :
            if v.etat==0 :
                L.append(v)
    return L

def update_mat (T):
    l=free_voxels(T)
    v=rd.choice(l)
    v.etat=1
    coord = v.coord[0], v.coord[1]
    T[coord[0],coord[1]]=v
    return T
    

    
    


    