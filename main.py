# Imports
import animation3D as a3de
from simulation import init_mat, update_mat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from scipy.stats import bernoulli
import time
from generation import *
from animation2D import generate_animation

# constantes
h, w, d = 100, 300, 100



def simulate(maxIter, animation=0, save=True, show=False, save_all=0):
    T  = init_mat(h,w,d,[np.ones((1,1,1), dtype=np.uint8)], [np.array([h//2,w//2,d//2])])
    
    if animation > 0 :
        # Fonction de mise à jour de la matrice de voxels
        def update(i):
            start = time.time()
            for _ in range(animation):
                update_mat(T, lambda T,L,orientations,_ : generation(T,L,orientations,masks, p_new), None)
            print(f"Frame {i+1} générée en {(time.time() - start)} secondes")
            return T
        # Fonction de mise à jour de la matrice de voxels avec arrêt après un certain nombre de frames
        def update_with_stop(_, i):
            if i >= maxIter/animation:
                plt.pause(30)
                return T  # Return the final state without further updates
            return update(i)

        # Génération de l'animation
        ani = a3de.generate_animation(T, update_with_stop, interval=100, show=show)

        # Enregistrement de l'animation
        ani.save('animation.gif', writer='pillow', fps=10)

    elif save_all > 0:
        # Fonction de mise à jour de la matrice de voxels
        def update(i):
            start = time.time()
            for _ in range(save_all):
                update_mat(T, lambda T,L,orientations,_ : generation(T,L,orientations,masks, p_new), None)
            temps = (time.time() - start)
            print(f"Frame {i+1} générée en {temps} secondes")
                 

        ims = []
        for i in range(maxIter//save_all):
            update(i)
            ims.append(T.copy())  # Append both matrices
        np.save("ims", ims)
        np.save("final", T)
        print("résultats enregistrés sous les noms ims.npy et final.npy")
        
    
    elif save :
        for _ in range(maxIter):
            update_mat(T, lambda T,L,orientations,_ : generation(T,L,orientations,masks, p_new), None)
        np.save("final", T)
        print("résultats enregistrés sous le nom final.npy")

        
        

def affichage(T, ims, direction, plan):
            """
            direction = 1 # Direction perpendiculaire au plan x, y, z pour directions 0, 1, 2 respectivement
            plan = 50  # Plan choisi, à savoir la variable x,y,z fixée à cette valeur
            """
            # Création d'une figure avec deux sous-graphes côte à côte
            fig = plt.figure(figsize=(14, 5))

            # Sous-graphe pour l'animation 2D
            ax1 = fig.add_subplot(1, 2, 1)
            print("Animation 2D en cours de génération...")
            ani = generate_animation(T, ims, direction, plan, interval=50, fig=fig, ax=ax1)

            # Sous-graphe pour l'image 3D
            print("Image 3D en cours de génération...")
            ax2 = fig.add_subplot(1, 2, 2, projection='3d')
            ax2.set_proj_type('ortho')
            ax2.set_box_aspect([h, w, d])
            ax2.set_xlim(0, h)
            ax2.set_ylim(0, w)
            ax2.set_zlim(0, d)

            valeur = plan  # Valeur du plan à afficher
            plan_mask = np.zeros((h, w, d), dtype=bool)
            # Création du plan à afficher selon la direction
            if direction == 0:  # Plan x
                plan_mask[valeur, :, :] = True
            elif direction == 1:  # Plan y
                plan_mask[:, valeur, :] = True
            else:  # Plan z
                plan_mask[:, :, valeur] = True

            base_cmap = plt.get_cmap('tab20', 20) # on sélectionne les 20 couleurs de la table 'tab20'
            colors = [base_cmap(i%20) for i in range (255)] # on récupère nos 256 couleurs (répétition des 20 couleurs)
            cmap = clrs.ListedColormap(colors)
                    

            rgba_colors = cmap(T) 
            rgba_colors[T == 0] = [0, 0, 0, 0] # on rend transparent le fluide qui a une valeur de 0
                
            ax2.voxels(T, facecolors=rgba_colors, alpha=0.5)
            ax2.voxels(plan_mask, facecolors='yellow', alpha=0.5)  # Plan en jaune

            plt.tight_layout()
            plt.show()

""" Attention, lors des simulations, le nombre d'image à générer pour obtenir un résultat convaincant peut grandement varier,
selon le bon vouloir de la fonciton scipy.stats.bernoulli.rvs"""
# Simuler et enregistrer la matrice finale
#simulate(2000, save=True)

# Simuler et enregistrer les matrices au fur et à mesure
simulate(400, save_all=10) #toutes les 10 matrices

# Simuler et enregistrer une animation
#simulate(2000, animation=10) #toutes les 10 matrices

# Afficher avec une coupe les fichiers enregistrés avec save_all=10
affichage(np.load("final.npy"), np.load("ims.npy"), 1, 150)