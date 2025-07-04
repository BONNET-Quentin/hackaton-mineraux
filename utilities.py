import numpy as np

theta = np.pi
R = np.array([[np.cos(theta),-np.sin(theta),0],[np.cos(theta),np.sin(theta),0],[0,0,1]])
T = np.array([[[0,0,0],
               [0,0,0],
               [0,0,0]],
              
              [[0,0,0],
               [1,0,1],
               [0,0,0]],

              [[0,0,0],
               [0,0,0],
               [0,0,0]]])

res = np.einsum('ai,bj,ck,ijk->abc', R, R, R, T)
res2 = np.einsum('ijk,kl->ijl', T,R)

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def mat (c : int):
    "fonction injective qui a une couleur codée en [1,255] renvoie une matrice de rotation, "
    "de préférence l'espace des rotation est couvert par [1,255]"
    Rx = np.array([[1, 0, 0],
                    [0, np.cos(2*np.pi*(c-1)/255), np.sin(2*np.pi*(c-1)/255)],
                    [0, -np.sin(2*np.pi*(c-1)/255), np.cos(2*np.pi*(c-1)/255)]
                    ])
    Ry = np.array([[np.cos(20*np.pi*(c-1)/255), 0, -np.sin(20*np.pi*(c-1)/255)],
                    [0, 1, 0],
                    [np.sin(20*np.pi*(c-1)/255), 0, np.cos(20*np.pi*(c-1)/255)]
                    ])
    Rz = np.array([[np.cos(200*np.pi*(c-1)/255), np.sin(200*np.pi*(c-1)/255), 0],
                    [-np.sin(200*np.pi*(c-1)/255), np.cos(200*np.pi*(c-1)/255),0],
                    [0, 0, 1],
                    ])
    return Rx@Ry@Rz


# prepare some coordinates
x, y, z = np.indices((8, 8, 8))

# draw cuboids in the top left and bottom right corners, and a link between
# them

vect = np.array([1, 1, 1])



cube = np.zeros((200, 200, 200), dtype = bool)

cube[125:175, 125:175, 125:175] = True




coul = np.linspace(0, 255, 256)
print(len(coul))
Vx, Vy, Vz = [], [], []
for c in coul :
    R = mat(c)
    vect_rot = R@(vect.T)
    Vx.append(vect_rot[0])
    Vy.append(vect_rot[1])
    Vz.append(vect_rot[2])


ax = plt.figure().add_subplot(projection='3d')

ax.scatter(Vx, Vy, Vz, marker = '*')
ax.set_title("Répartition des changements d'orientation possibles")

plt.show()
