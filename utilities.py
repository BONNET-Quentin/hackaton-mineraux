# Fichier pour toutes les fonctions de représentation etc

# Imports des autres fonctions
import numpy as np
from classes import *
from utilities import *
from numpy import random

# Paramètres
N = 10  # Nombre d'itérations
M = 1  # Nombre de cristaux
taille_cristal = 10  # Taille du cristal

# Initialisation des cristaux
matrice = Cristal()

# Génération d'un voxel aléatoire
def initialisation_voisins(matrice):
    for voxel in matrice:
        if voxel.etat == 1:
            direction = np.array([-1, -1]), np.array([1, 1]), np.array([-1, 1]), np.array([1, -1])
            for dir in direction:
                x = (voxel.coord + dir)[0]
                y = (voxel.coord + dir)[1]
                if matrice[x][y].etat == 1:
                    voxel.voisins.append(matrice[x][y])
                else:
                    voxel.libre.append(matrice[x][y])
    return

def generer_voxel(matrice):
    # On choisit un voxel aléatoire dans la liste des voxels libres
    voxel_choisi = random.choice(matrice)
    while voxel_choisi.etat == 0 or len(voxel_choisi.libre) != 0:  # On s'assure que le voxel est libre
        voxel_choisi = random.choice(matrice)
        
    # Génère une nouvelle coordonnée aléatoire pour le voxel
    nouveau_voxel = random.choice(voxel_choisi.libre) # On prend une place libre du voxel choisi
    voisins = voisins_voxel(matrice, nouveau_voxel)  # On récupère les voisins du voxel généré
    for voisin in voisins:
        if voisin.etat == 1:
            voisin.libre.remove(nouveau_voxel)
            voisin.voisins.append(nouveau_voxel)
            nouveau_voxel.voisins.append(voisin)
        else:
            nouveau_voxel.libre.append(voisin)
    return

def voisins_voxel(matrice, voxel):
    voisins = []
    direction = np.array([-1, -1]), np.array([1, 1]), np.array([-1, 1]), np.array([1, -1])
    for dir in direction:
        x = (voxel.coord + dir)[0]
        y = (voxel.coord + dir)[1]
        if matrice[x][y].etat == 1:
            voisins.append(matrice[x][y])
    return voisins
