# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# constantes
h, L = 50,50

# initialisation de la figure
fig,ax = plt.subplots()

# génération d'une liste de tableaux de booléens de taille (h, L) à afficher
matrix = np.zeros((h,L), dtype=bool)
ims = []
for i in range(60):
    matrix = (1-matrix)
    im = ax.imshow(matrix, animated=True, cmap='gray', vmin=0, vmax=1)
    if i == 0:
        ax.imshow(matrix, cmap='gray', vmin=0, vmax=1)  # show an initial one first
    ims.append([im])

# animation
ani = animation.ArtistAnimation(fig, ims, interval=1000, blit=True,
                                repeat_delay=1000)

# affichage
plt.show()