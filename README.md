# hackaton-mineraux

Le but de ce hackaton est de simuler la génération de cristaux solides dans une matrice liquide : un procédé stochastique de croissance. 

Pour les principes de base on part d'une modélisation sous forme d'une matrice de booléens (True si c'est un solide/précipité et False si c'est un liquide). Ci-dessous l'ordre de réalisation du projet, qu'on simplifie au départ pour avoir des programmes qui compilent, et qu'on complexifie derrière pour rajouter des modélisations/optimisations. Les versions d'intêret sont : version 6 avec génération aléatoire et croissance isotrope avec des couleurs, la version 7 avec la coupe du plan 2D avec génération aléatoire et croissance isotrope avec des couleurs, la version 8 avec anisotropie simple sans génération aléatoire, la version 9 qui lui rajoute l'analyse 2D. 

Même si tout est organisé dans des dossiers sous forme de versions (car les commit sont très nombreux et confus), le hash du commit de la version finale est : .

La plupart des versions fonctionnent juste en compilant le code main.py. En ce qui concerne les bibliothèques, tout est sur du numpy, matplotlib et scipy (assez classiques, les installations déjà faites auparavants dans l'UE était suffisant sans faire de pip install). Le seul problème reste le mp4 avec ffmpeg mais comme on le verra plus tard il n'est pas très utile sachant qu'on a le .gif

-La première tâche était de créer une croissance en 2D. La partie complexe était avant tout de partir d'un cristal initial, et de générer les cristaux en faisant attention de repérer les points de croissance (donc les solides dans la matrice, qui nécessite un scan couteux en complexité de la matrice), en créant des points qui n'existaient psa déjà (on ne peut pas faire pousser à l'intérieur d'un cristal...). La croissance à partir de maintenant se fera de manière isotrope, on verra plus tard des directions privilégiées de croissance.

-Ensuite on a généralisé ce programme pour qu'il puisse s'animer également en 3D (c'est la version 1). Il se base sur la détermination des voisins libres pour croissance autour d'un solide.

-Une autre proposition de programme (version 2) a été proposée qui évite de recalculer ces voisins libres à chaque fois comme fait précédemment. Ces deux algorithmes ne nécessitent pas plus d'attention il n'étaient pas très bien optimisés.

-Ensuite, on a décidé de pouvoir garder une trace animée de cette génération 3D à l'aide de deux versions différentes, la première la version 3 en mp4 qui marche moins bien.

-La deuxième (version 4) fonctionne avec des gif et ne nécessite pas des installations techniques de ffmpeg etc. elle s'utilise directement avec matplotlib. Il y a toujours des incompris car le gif ne "filme" parfois que la fin de la croissance, et est également très couteuse en génération d'images, à où le calcul de la matrice est très rapide. De manière générale ce qui va causer des problèmes de lenteur c'est la génération en 3D et l'enregistrement de l'animation 3D, moins que le code en lui-même (même si on va l'optimiser juste après).

-La version 5 s'occupe de pouvoir partir de génération plus aléatoires : au lieu de partir d'un cube classique comme avant, on génère aussi des billes et des pavés de manière aléatoire dans la matrice, au nombre qu'on veut. De plus les cristaux de croissance 

-La version 6 s'occupe d'optimiser le programme de génération, en utilisant la puissance de numpy et les booléens afin de faire diminuer la complexité, car les boucles for restent du python alors que la strucutre numpy est en C++, ce qui permet des meilleurs temps de calcul. Sans rentrer dans les détails on gagne 6 fois en performance.

-La version 7 introduit une coupe selon un plan 2D dans une génération de type aléatoire de billes et pavés, avec une possibilité de choisir le plan en question. Pour cela il faut utiliser main_2D pour la coupe, mais main classique marche toujours. Le temps de génération est pas contre assez long il faut être un pue patient...matplotlib demande une grosse capacité de calcul pour générer les images. Le but est de pouvoir reproduire ce qu'on visualise quand on découpe un matériau et qu'on visualise la précipitation de ce dernier dans une tranche au microscope. 

-La version 8 permet d'ajouter la croissance anisotrope, mais se restreint à un seul cristal de départ non aléatoire, cependant il a déjà une meilleure forme de cristal. La version est également optimisée afin de combler les trous des géénrations (plus grande proba de générer si on a des voisins solides) là où dans les anciens codes on se retrouvait avec des excroissances étranges.

-La version 9 fusionne la version 7 et 9 pour pouvoir visualiser l'animation de la découpe en 2D de la croissance anisotrope.

-La version 10 intègre des directions de générations en utilisant des masques de croissance et de rotation dans la matrice, pour générer des excroissances qui donnent plus l'air d'une croissance anisotrope aléatoire (pas selon des directions orthogonales simples) tout en rajoutant des couleurs selon l'orientation de la croissance.

# Bijection utilisée entre $[|1,n^3|]$ et $[|1,n|]\times[|1,n|]\times[|1,n|]$ :
$$f_n : [|0,n^3-1|] \to [|0,n-1|]\times[|0,n-1|]\times[|0,n-1|], k \mapsto (k//n^2, (k\%n^2)//n, (k\%n^2)\%n)$$

$$f_n^{-1} (x,y,z) = n^2*x + n*y + z$$