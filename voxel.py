import numpy as np
import random as rd 

# Fichier pour créer les classes

class voxel :
    def __init__(self,coord,etat,voisins,p):
        self.coord=coord
        self.etat=etat
        self.voisins=voisins
      
@np.vectorize 
def get_etat(v:voxel):
    return v.etat
    
    
def init_mat (h,w,d,n):
    
    T=np.zeros((h,w,d), dtype=object)
    
    for i in range (h):      ##on définit la matrice 
            for j in range (w):
                for k in range (d):
                    v=voxel((i,j,k),0,[],[])
                    T[i,j,k]=v
            
            
    s=h//2-n//2
    f=w//2-n//2
    r=d//2-n//2
    
    for i in range (s,s+n):     ##on définit le cristal
        for j in range (f,f+n):
            for k in range (r,r+n):
                T[i,j,k].etat=1
            
    
    for i in range (h) :
        for j in range (w) :
            for k in range(d) :
                l=[]
                if i+1<h:
                    l.append(T[i+1,j,k])
                if j-1>0:
                    l.append(T[i,j-1,k])
                if j+1<w:
                    l.append(T[i,j+1,k])
                if i-1>0: 
                    l.append(T[i-1,j,k])
                if k+1<d:
                    l.append(T[i,j,k+1])
                if k-1>0:
                    l.append(T[i,j,k-1])
                T[i,j,k].voisins=l
    
    return T

    
def conv (T):  ##fait un tableau affichable à partir du tableau de voxel 
    h,w,d=T.shape
    A=np.zeros((h,w,d),dtype=bool)
    for i in range (h):
        for j in range (w):
            for k in range (d):
                A[i,j,k]=T[i,j,k].etat
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
    T[v.coord[0],v.coord[1],v.coord[2]]=v
    return T
    

    
    


    