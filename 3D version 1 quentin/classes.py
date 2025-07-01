import numpy as np

# Fichier pour créer les classes

class voxel :
    def __init__(self,coord,etat,voisins,libre):
        self.coord=coord
        self.etat=etat
        self.voisins=voisins
        self.libre=libre
    
    def afficher_libre(self):
        print(self.libre)

def init_mat (h,L,l,n):
    
    T=np.zeros((h,L,l), dtype=object) 
    
    for i in range (h):      ##on définit la matrice 
            for j in range (L):
                for k in range (l):
                    v=voxel((i,j,k),0,[],[])
                    T[i,j,k]=v
            
            
    s=L//2-n//2
    f=h//2-n//2
    r=l//2-n//2
    
    for i in range (s,s+n):     ##on définit le cristal
        for j in range (f,f+n):
            for k in range (r,r+n):
                T[i,j,k].etat=1
    
    for i in range (h) :
        for j in range (L) :
            for k in range (l):
                liste=[]
                if i+1<h:
                    liste.append(T[i+1,j,k])
                if i-1>=0:
                    liste.append(T[i-1,j,k])
                if j+1<L:
                    liste.append(T[i,j+1,k])
                if j-1>=0:
                    liste.append(T[i,j-1,k])
                if k+1<l:
                    liste.append(T[i,j,k+1])
                if k-1>=0:
                    liste.append(T[i,j,k-1])
                T[i,j,k].voisins=liste

    return T

    
def conv (h, L, l, T):  ##fait un tableau affichable à partir du tableau de voxel 
    A = np.zeros((h, L, l))
    for i in range(h):
        for j in range(L):
            for k in range(l):
                A[i, j, k] = T[i, j, k].etat
    return A

    