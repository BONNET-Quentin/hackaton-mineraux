import numpy as np

# Fichier pour créer les classe

class voxel :
    def __init__(self,coord,etat,voisins):
        self.coord=coord
        self.etat=etat
        self.voisins=voisins
    
def init_mat (h,L,n):
    
    T=np.zeros((h,L))
    
    for i in range (h):      ##on définit la matrice 
            for j in range (L):
                v=voxel((i,j),0)
                T[i,j]=v
            
            
    s=int(L/2)-int(L/2)
    f=int(L/2)+int(L/2)
    
    for i in range (s,f):     ##on définit le cristal
        for j in range (s,f):
            T[i,j].etat=1
    
    for i in range (h) :
        for j in range (L) :
            l=[]
            if i+1<=h:
                l.append(T[i+1,j])
            if j-1>=0:
                l.append(T[i-1,j])
            if j+1<=L:
                l.append(T[i,j+1])
            if i-1>0: 
                l.append(T[i-1,j])
            T[i,j].voisins=l
    
    return T

    
def conv (h,L,T):  ##fait un tableau affichable à partir du tableau de voxel 
    A=np.zeros((h,L))
    for i in range (h):
        for j in range (L):
            A[i,j]=T[i,j].etat
    return A 
            
        
    
        

    