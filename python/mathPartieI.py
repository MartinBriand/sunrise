# coding: utf8

# On suppose que l'on a une série de points en entrée, on s'occupera
# de ce détail plus tard.
# On considère le pas de temps comme imposé dans la cadre arduino

import numpy as np
import matplotlib.pyplot as plt
import math
from pylab import *

############### Première partie : Discrétisation de la trajectoire ############

print("\n### Première partie : Discrétisation de la trajectoire ###\n")

# 3 longeurs en m
pas_translation_x = 0.01
pas_translation_y = 0.01
pas_translation_z = 0.01
# 3 angles en radian
pas_rotation_alpha = 3.14/180
pas_rotation_beta = 3.14/180
pas_rotation_gamma = 3.14/180
# vecteur des pas maximaux que l'on s'autorise
pas_maximal = np.array([pas_translation_x, pas_translation_y,
                        pas_translation_z, pas_rotation_alpha,
                        pas_rotation_beta, pas_rotation_gamma])

print("pas_translation_x :  %.3f m" % pas_translation_x)
print("pas_translation_y :  %.3f m" % pas_translation_y)
print("pas_translation_z :  %.3f m" % pas_translation_z)
print("pas_rotation_alpha : %.4f rad" % pas_rotation_alpha)
print("pas_rotation_beta :  %.4f rad" % pas_rotation_beta)
print("pas_rotation_gamma : %.4f rad" % pas_rotation_gamma)


def calcul_pas_adapte(trajectoire, pas_maximal):
    """
    Donne le nombre de pas à effectuer pour chaque dimension pour une étape
    dans la trajectoire.

    Pour calculer le pas adapté, on calcule le nombre de pas minimal que l'on
    devra faire pour aller de la source à la destination (la dimension dont le
    pas est le plus petit dicte le nombre de pas).

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Vecteur de taille 9 des pas pour chaque intervalle
    :rtype: np.array
    """

    nb_intervalles = len(trajectoire) - 1
    nombre_pas = np.zeros(nb_intervalles, dtype=int)

    for j in range(nb_intervalles):
        nombre_pas_detail = np.zeros(6)
        for i in range(6):
            nombre_pas_detail[i] = abs(trajectoire[j+1][i] -
                                       trajectoire[j][i]) / pas_maximal[i]
        nombre_pas[j] = math.ceil(np.amax(nombre_pas_detail))
    return nombre_pas


def discretisation_trajectoire(trajectoire, pas_maximal):
    """
    Discrétise la trajectoire souhaitée en divisant les parties trop grandes en
    pas de longueurs constantes par morceaux plus petits que pas_maximal.
    Renvoie 2 listes :
    1. la liste des points par lesquels il faut passer, inutile pour les
    moteurs mais utile pour tracer les courbes de trajectoire ;
    2. la liste des déplacements infinitésimaux qu'il faut pour passer d'un
    point à un autre. Chacun de ces déplacements infintésimaux est un np.arra
    de 6 dimensions, 3 en position et 3 angulaires.

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Couple d'arrays
    :rtype: (np.array, np.array)
    """

    nb_intervalles = len(trajectoire) - 1
    nombre_pas = calcul_pas_adapte(trajectoire, pas_maximal)

    traj_disc = np.zeros((1, 6))
    var_disc = np.zeros((1, 6))
    # traj_disc = np.empty((1, 6))
    # var_disc = np.empty((1, 6))

    for j in range(nb_intervalles):
        nb_pas_j = nombre_pas[j]

        dx = (trajectoire[j+1][0] - trajectoire[j][0]) / nb_pas_j
        dy = (trajectoire[j+1][1] - trajectoire[j][1]) / nb_pas_j
        dz = (trajectoire[j+1][2] - trajectoire[j][2]) / nb_pas_j
        dalpha = (trajectoire[j+1][3] - trajectoire[j][3]) / nb_pas_j
        dbeta = (trajectoire[j+1][4] - trajectoire[j][4]) / nb_pas_j
        dgamma = (trajectoire[j+1][5] - trajectoire[j][5]) / nb_pas_j

        for i in range(0, nb_pas_j):
            x = trajectoire[j][0] + i * dx
            y = trajectoire[j][1] + i * dy
            z = trajectoire[j][2] + i * dz
            alpha = trajectoire[j][3] + i * dalpha
            beta = trajectoire[j][4] + i * dbeta
            gamma = trajectoire[j][5] + i * dgamma

            traj_disc = np.append(traj_disc,
                                  [[x, y, z, alpha, beta, gamma]],
                                  axis=0)
            var_disc = np.append(var_disc,
                                 [[dx, dy, dz, dalpha, dbeta, dgamma]],
                                 axis=0)

    return traj_disc, var_disc


##################### Deuxième partie : Longueur des câbles ###################

print("\n### Deuxième partie : Longueur et variation de longueur des câbles ###\n")

# Convertit les déplacements infintésimaux du mobile en variations de longueurs
# des câbles en utilisant des matrices de rotation.


def construction_mobile(dimensions):
    """
    Renvoie la liste de taille 8 des coordonnées des points du mobile ; chaque
    coordonnée de coin du rectangle sera un array de taille 3 (x, y et z).
    Attention, les croisements ne sont pas pris en compte.

    :param dimensions: dimensions physiques du mobile que l'on souhaite
    construire, array de dimension 3 (x, y et z)

    :type dimensions: np.array

    :return: liste de taille 8 des coordonnées des points du mobile
    :rtype: np.array
    """
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    A6 = np.array([-lx/2, -ly/2, -lz/2])
    A7 = np.array([-lx/2, -ly/2, lz/2])
    A5 = np.array([-lx/2, ly/2, lz/2])
    A4 = np.array([-lx/2, ly/2, -lz/2])
    A0 = np.array([lx/2, -ly/2, -lz/2])
    A1 = np.array([lx/2, -ly/2, lz/2])
    A3 = np.array([lx/2, ly/2, lz/2])
    A2 = np.array([lx/2, ly/2, -lz/2])

    mobile = [A0, A1, A2, A3, A4, A5, A6, A7]
    return mobile


def construction_hangar(dimensions):
    """
    Renvoie la liste de taille 8 des coordonnées des points du hangar ; chaque
    coordonnée de coin du rectangle est un array de taille 3 (x, y et z).
    Le coin A6 doit être placé à l'origine.

    :param dimensions: dimensions physiques du hangar que l'on souhaite
    construire, array de dimension 3 (x, y et z)

    :type trajectoire: np.array

    :return: liste de taille 8 des coordonnées des points du hangar
    :rtype: np.array
    """
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    A6 = np.array([0, 0, 0])
    A7 = np.array([0, 0, lz])
    A5 = np.array([0, ly, lz])
    A4 = np.array([0, ly, 0])
    A0 = np.array([lx, 0, 0])
    A1 = np.array([lx, 0, lz])
    A3 = np.array([lx, ly, lz])
    A2 = np.array([lx, ly, 0])

    hangar = [A0, A1, A2, A3, A4, A5, A6, A7]
    return hangar


def construction_rectangle(dimensions, centre):
    # à supprimer

    # dimensions contient les dimensions physiques du pavé que l'on souhaite
    # construire. Il s'agit d'un np.array de dimension 3 (x, y et z).
    # centre est un booleen qui indique si l'on doit placer le centre du
    # rectangle sur l'origine ou plutôt le coin A6. True signifie que le centre
    # doit être placé à l'origine (pour le mobile) et False signifie que le
    # coin A6 doit être placé à l'origine.

    # Cette fonction annexe mais utile est celle que vous avez défini dans
    # votre code comme coinHangar. Je pense qu'elle va effectivement vous
    # permettre d'avoir un code plus simple à lire.

    # Cette fonction renvoie une liste de taille 8 des coordonnées des points
    # du rectangle collé contre l'origine et orienté comme le hangar. Chaque
    # coordonnée de coin du rectangle sera un np.array de dimension 3
    lx = dimensions[0]
    ly = dimensions[1]
    lz = dimensions[2]

    if centre:  # attention, croisement pas pris en compte
        A6 = np.array([-lx/2, -ly/2, -lz/2])
        A7 = np.array([-lx/2, -ly/2, lz/2])
        A5 = np.array([-lx/2, ly/2, lz/2])
        A4 = np.array([-lx/2, ly/2, -lz/2])
        A0 = np.array([lx/2, -ly/2, -lz/2])
        A1 = np.array([lx/2, -ly/2, lz/2])
        A3 = np.array([lx/2, ly/2, lz/2])
        A2 = np.array([lx/2, ly/2, -lz/2])

    else:
        A6 = np.array([0, 0, 0])
        A7 = np.array([0, 0, lz])
        A5 = np.array([0, ly, lz])
        A4 = np.array([0, ly, 0])
        A0 = np.array([lx, 0, 0])
        A1 = np.array([lx, 0, lz])
        A3 = np.array([lx, ly, lz])
        A2 = np.array([lx, ly, 0])
    mobile = [A0, A1, A2, A3, A4, A5, A6, A7]
    return mobile


def rotation(vecteur_rotation):
    """
    Renvoie la matrice de rotation associée aux angles de rotation.
    Multiplier un vecteur par la matrice de rotation permettra de lui faire
    subir les trois rotations.

    :param vecteur_rotation: vecteur des 3 angles de rotation.
    rho, theta et phi sont des déplacements angulaires du mobile autour des
    trois vecteurs de la base du hangar.

    :type vecteur_rotation: np.array de taille 3

    :return: produit des trois matrices de rotations données respectivement
    par les angles rho, theta, et phi
    :rtype: np.array de dimension 3x3
    """
    rho = vecteur_rotation[0]
    theta = vecteur_rotation[1]
    phi = vecteur_rotation[2]

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rho), np.sin(rho)],
                   [0, -np.sin(rho), np.cos(rho)]])

    Ry = np.array([[np.cos(theta), 0, -np.sin(theta)],
                   [0, 1, 0],
                   [np.sin(theta), 0, np.cos(theta)]])

    Rz = np.array([[np.cos(phi), np.sin(phi), 0],
                   [-np.sin(phi), np.cos(phi), 0],
                   [0, 0, 1]])

    return np.dot(np.dot(Rx, Ry), Rz)


def reconstruction_coins(position_mobile, dimensions_mobile):
    """
    Calcule la liste des positions des 8 coins du mobile à partir des
    dimensions et des coordonnées du centre du mobile.
    Renvoie la liste des positions des 8 coins. Chaque position est un
    np.array de taille 3 (x, y, z).
    On appelle cette fonction à chaque fois que l'on change les
    coordonnées du mobile.
    Méthode :
    1. Création du mobile de bonnes dimensions mais en faisant coincider le
    centre du mobile avec le centre du repère du hangar ;
    2. Orientation du mobile pour qu'il soit aligné avec l'orientation donnée
    par base_mobile (en utilisant des matrices de rotation pour arriver à

    #######################################
    ##### Qu'est ce que base_mobile ? ##### position_mobile[3:6]
    #######################################

    l'orientation souhaitée depuis l'orientation d'origine du hangar) ;
    3. Déplacement du mobile pour que son centre se retrouve à la position
    donnée par position_mobile.

    A faire : passer mobile en argument ?

    :param position_mobile: np.array de taille 6 (3 positions, 3 angles)
    représentant la position actuelle du centre du mobile et son orientation.
    :param dimensions_mobile: np.array de taille 3 (longueur, largeur, hauteur)
    représentant les dimensions physiques du mobile.

    :type position_mobile: np.array de taille 6
    :type dimensions_mobile: np.array de taille 3

    :return: liste de 8 éléments des positions des huits coins
    :rtype: liste
    """

    # 1.
    mobile = construction_mobile(dimensions_mobile)

    # 2
    orientation = position_mobile[3:6]
    rotation_mobile = rotation(orientation)

    # 3
    translationCentre = position_mobile[0:3]

    for coord in range(8):
        mobile[coord] = np.dot(rotation_mobile, mobile[coord])  # 2
        mobile[coord] += translationCentre  # 3

    return mobile


def calcul_longueurs_cables(pos_coins_mobile, pos_coins_hangar):
    """
    Renvoie les longueurs des 8 câbles correspondant à la position du mobile
    dans le hangar.
    Les câbles étant croisés dans le hangar, on introduit en (a) une liste de
    changements d'indices.

    :param pos_coins_mobile: liste des positions des 8 coins du mobile, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.
    :param pos_coins_hangar: liste des positions des 8 coins du hangar, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.

    #########################
    ##### Quel schéma ? #####
    #########################

    :type pos_coins_mobile: np.array
    :type pos_coins_hangar: np.array

    :return: vecteur des longueurs des 8 câbles
    :rtype: np.array de taille 8
    """

    longueurCable = np.zeros(8)
    # (a)
    chgt_num = [6, 7, 4, 5, 2, 3, 0, 1]

    for cable in range(8):
        vecteurCoins = pos_coins_mobile[chgt_num[cable]] - pos_coins_hangar[cable]
        longueurCable[cable] = np.linalg.norm(vecteurCoins)

    return longueurCable


def commande_longeurs_cables(traj_disc, dimensions_mobile, dimensions_hangar):
    """
    Convertit la trajectoire discrétisée (liste des déplacements infinitésimaux
    qu'il faut réaliser pour parcourir la trajectoire souhaitée) en la liste
    des modifications infinitésimales des longueurs des câbles.

    Pour cela, on doit garder en mémoire (dans des variables locales) la
    position actuelle du module (6 valeurs), ainsi que les longueurs actuelles
    des cordes.

    Pour chaque déplacement infinitésimal dans cette boucle on devra :
    1. Mettre à jour la position mémorisée du mobile (selon les 6 dimensions) ;
    2. Reconstruire les coins du mobile (en prenant en compte l'orientation
    avec reconstruction_coins) ;
    3. Calculer les nouvelles longueurs des cordes ;
    4. En déduire les variations des longueurs des cordes par rapport à celles
    de l'état précédent ;
    5. Mettre à jour les longueurs des cordes.


    :param traj_disc: trajectoire discrétisée dans la première partie du code,
    chaque point de la trajectoire est un np.array de taille 6.
    :param dimensions_mobile: np.array de taille 3 (longueur, largeur, hauteur)
    représentant les dimensions physiques du mobile.
    :param dimensions_hangar: np.array de taille 3 (longueur, largeur, hauteur)
    représentant les dimensions physiques du hangar.

    :type traj_disc: np.array de taille 6
    :type dimensions_mobile: np.array de taille 3
    :type dimensions_hangar: np.array de taille 3

    :return: liste des variations des longueurs des cordes, chaque élément de
    la liste étant un np.array de dimension 8 dont le ième élément est la
    variation de longueur de la ième corde ; liste des longeurs des cordes pour
    chaque itération.
    :rtype: (np.array, np.array)
    """

    coinsHangar = construction_hangar(dimensions_hangar)

    # objectif : nombre de pas total
    nombreIteration = len(traj_disc[1])
    # ATTENTION JE NE SAIS PAS SI CA FONCTIONNE ET C'EST UN DETAIL IMPORTANT
    positionInitiale = traj_disc[0][0]
    coinsPositionInit = reconstruction_coins(positionInitiale, dimensions_mobile)

    longueursCableInit = calcul_longueurs_cables(coinsPositionInit, coinsHangar)
    tableauVarLongueur = []
    tableauLongueur = []  # test

    for dt in range(1, nombreIteration):

        nouvellePosition = positionInitiale + traj_disc[1][dt]
        coinsNouvellePosition = reconstruction_coins(nouvellePosition,
                                                     dimensions_mobile)
        nouvellesLongueursCables = calcul_longueurs_cables(
                                    coinsNouvellePosition, coinsHangar)
        variationLongueur = nouvellesLongueursCables - longueursCableInit
        tableauVarLongueur.append(variationLongueur)
        tableauLongueur.append(nouvellesLongueursCables)  # test
        longueursCableInit = nouvellesLongueursCables
        positionInitiale = nouvellePosition

    # on retourne une liste des variations de longueur des cables
    return tableauLongueur, tableauVarLongueur


# Définir la trajectoire
# origine = np.array([0, 0, 0, 0, 0, 0])
# destination = np.array([0.5, 0.5, 0.5, 0, 0, 0])

# trajectoire = np.array([origine], dtype=float)
# trajectoire = np.insert(trajectoire, 1, destination, 0)
trajectoire = np.random.rand(10, 6)
# print("Trajectoire : %s" % trajectoire)
centre = np.array([0, 0, 0, 0, 0, 0])
dimension = np.array([0.25, 0.25, 0.3])
print("Dimensions du mobile : %s" % dimension)
coinsMobile = (reconstruction_coins(centre, dimension))


dimensionHangar = np.array([1.25, 1.25, 1])
print("Dimensions du hangar : %s" % dimensionHangar)
coinsHangar = construction_hangar(dimensionHangar)
# print(calcul_longueurs_cables(coinsMobile, coinsHangar))

longueurCable, varlongueurCable = commande_longeurs_cables(
            discretisation_trajectoire(trajectoire, pas_maximal),
            dimension,
            dimensionHangar)


n = len(varlongueurCable)
# print(n)


temps = list(range(n))


print("\nTracé des courbes...")
# Tracé des variations de longueur des câbles i
plt.subplot(1, 2, 1)
for cable in range(8):
    plt.plot(temps,
             [varlongueurCable[i][cable] for i in range(n)],
             label='Cable '+str(cable))

plt.legend()

# Tracé des longueurs des câbles i
plt.subplot(1, 2, 2)
for cable in range(8):
    plt.plot(temps,
             [longueurCable[i][cable] for i in range(n)],
             label='Cable '+str(cable))

plt.legend()
plt.show()


######################## Troisième partie : Commande du robot #################

print("\n### Troisème partie : Commande du robot ###\n")


def commande(trajectoire, pas_maximal, dimensions_mobile, dimensions_hangar):
    # Les définitions de tous les arguments sont données respectivement dans
    # discretisation_trajectoire, calcul_pas_adapte, reconstruction_coins,
    # commande_longeurs_cables

    # Cette fonction est la fonction de haut niveau dont on se servira pour
    # commander la maquette.
    # Elle prend en argument la trajectoire souhaitée et renvoie la commande à
    # passer aux moteurs.
    # Ces étapes de fonctionnement sont :
    # - 1 : On discrétise la trajectoire donnée en argument.
    # - 2 : On déduit de la trajectoire discrétisée les variations de longueurs
    # des câbles.
    # - 3 : On traduit ces variations de longueur des câbles en commande de
    # rotation angulaire des moteurs.

    # Cette fonction renvoie une liste des commandes des moteurs. Chaque
    # commande moteur sera à son tour un np.array de dimension 8 dont le ième
    # élément sera la commande destinée au ième moteur.

    diametreTambour = 0.009
    _, trajectoireDiscretisee = discretisation_trajectoire(trajectoire,
                                                           pas_maximal)
    longueurCable, _ = commande_longeurs_cables(trajectoireDiscretisee,
                                                dimensions_mobile,
                                                dimensions_hangar)
    nombrePosition = len(longueurCable)
    rotationMoteur = []
    for i in range(nombrePosition):
        rotation = np.arctan(longueurCable[i]/diametreTambour)
        rotationMoteur += [rotation]

    return rotation


# origine = np.array([0., 0., 0., 0., 0., 0.])
# destination = np.array([0.5, 0., 0., 0, 0, 0])
# n = calcul_pas_adapte(origine, destination, pas_maximal)


######################## Quatrième partie : Initialisation ##################

print("\n### Quatrième partie : Initialisation de la maquette ###\n")

# L'objectif de cette partie est de faire l'initialisation visuelle de la
# maquette. Pour cela on aura un bouton et un numéro du moteur on pourra donc
# faire tourner manuellement le moteur


def initialisationRotation(numeroMoteur, bouton):
    # cette fonction prend en argument le numéro du moteur qui est un entier et
    # un bouton qui est fait un True/False
    diametreTambour = 0.009
    rotationMoteur = [0 for k in range(8)]
    if bouton:
        rotationMoteur = math.arctan(0.01/diametreTambour)
    return rotationMoteur
