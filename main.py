# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from animation import generate_animation, example_matrices
from classes import init_mat, conv

# constantes
h, L = 50,50
n = 5 # taille du cristal initial

T = init_mat(h, L, n)
A = conv(h, L, T)

generate_animation([A], interval=500)