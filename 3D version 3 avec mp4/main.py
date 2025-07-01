# Imports
from animation import generate_animation, example_matrices
import animation3D as a3d
from voxel import init_mat, conv, update_mat

import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'
from matplotlib.animation import FFMpegWriter

# constantes
h, w, d = 30,30,30
n = 1

# initialisation de la matrice
T = init_mat(h, w, d, n)

# Fonction de mise à jour
def update(i):
    for _ in range(10):
        update_mat(T)
    print(f"Frame {i}")
    return conv(T)

MAX_FRAMES = 100

def update_with_stop(_, i):
    if i >= MAX_FRAMES:
        plt.pause(30)
        return conv(T)  # Return the final state without further updates
    return update(i)

# Génération de l'animation
fig, ani = a3d.generate_animation(conv(T), update_with_stop, interval=100, return_fig=True)

# Enregistrement de l'animation
# PROCEDURE : il faut installer ffmpeg et le mettre dans le PATH
# https://ffmpeg.org/download.html
# Ensuite quand on lance le scirpt, il faut fermer la fenetre de visualisation, et laisser tourner le programme puis CTRL C
writer = FFMpegWriter(fps=10, bitrate=1800) # essayer 10fps, sinon 100 fps marche mais il faudra ralentir la vidéo
ani.save("animation.mp4", writer=writer)
