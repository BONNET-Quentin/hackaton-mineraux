# Fichier pour toutes les fonctions de représentation etc

# Imports des autres fonctions
import numpy as np
from classes import *
from utilities import *
from numpy import random

# Génération d'un voxel aléatoire
def initialisation_voisins(matrice):
    for voxel in matrice.flatten():
        libres = []
        for voisin in voxel.voisins:
            if voisin.etat == 0:
                libres.append(voisin)  # On ajoute le voisin libre à la liste des voisins du voxel
                voxel.libre = libres  # On met à jour la liste des voxels libres du voxel
        matrice[voxel.coord[0], voxel.coord[1]] = voxel  # On met à jour le voxel dans la matrice 
    return

def generer_voxel(matrice):
    # On crée un masque pour ne garder que les voxels ayant des voisins libres
    voxels_avec_libres = [voxel for voxel in matrice.flatten() if voxel.etat == 1 and voxel.libre != []]
    if voxels_avec_libres == []:
        return  # Aucun voxel disponible
    voxel_choisi = random.choice(voxels_avec_libres)
        
    # Génère une nouvelle coordonnée aléatoire pour le voxel
    nouveau_voxel = random.choice(voxel_choisi.libre) # On prend une place libre du voxel choisi
    voisins = nouveau_voxel.voisins  # On récupère les voisins du voxel généré
    for voisin in voisins:
        if voisin.etat == 1:
            if nouveau_voxel in voisin.libre:
                voisin.libre.remove(nouveau_voxel)
        else:
            nouveau_voxel.libre.append(voisin)
    nouveau_voxel.etat = 1  # On change l'état du voxel généré à 1 (occupé)
    return

