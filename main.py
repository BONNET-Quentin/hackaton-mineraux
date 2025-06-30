# Imports
from animation import generate_animation, example_matrices
from voxel import init_mat, conv, update_mat


# constantes
h, L = 50,50
n = 5 # taille du cristal initial
nb_im=10

T = init_mat(h, L, n)
A = conv(h, L, T)

I=[]
I.append(A)

for i in range(nb_im):
    T=update_mat(T)
    im=conv(h, L, T)
    I.append(im)

generate_animation(I, interval=500)