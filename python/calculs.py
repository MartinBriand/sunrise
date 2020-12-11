# coding: utf8
#bonjour
import numpy as np
import time
import math

import modules.objects as obj

print(">> Running calculs.py...")

# VARIABLES #

# Hangar
hangar_x = 1.25
hangar_y = 1.25
hangar_z = 1
dimensions_hangar = np.array([hangar_x, hangar_y, hangar_z])
# Mobile
mobile_x = .25
mobile_y = .25
mobile_z = .3
dimensions_mobile = np.array([mobile_x, mobile_y, mobile_z])

# Trajectoire
# array_trajectory = np.random.rand(10, 6)
array_trajectory = np.array([[0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0]])
# maximal steps authorized
max_step_x = 0.1
max_step_y = 0.1
max_step_z = 0.1
max_step_alpha = math.radians(10)
max_step_beta = math.radians(10)
max_step_gamma = math.radians(10)
# array
max_step = np.array([max_step_x, max_step_y, max_step_z,
                     max_step_alpha, max_step_beta, max_step_gamma])


# DISPLAY #
display = False
dim6d = ['x ', 'y ', 'z ', 'alpha', 'beta ', 'gamma']
typedim = ['translation', 'rotation']
units = ['m', 'rad']


# PART 1 : TRAJECTORY DISCRETIZATION #

def calcul_nb_steps(trajectory, max_step):
    """
    For each interval of the trajectory, gives the number of steps into which
    we are going to discretize it.

    If j is the inverval we consider, we compute the number of steps we have to
    do for each dimension in j, and we take the maximum of these numbers. The
    biggest number of steps (i.e. the lowest step) is then conserved.

    :param trajectory: trajectory we want the mobile to follow
    :param max_step: maximal step for each dimension

    :type trajectory: Trajectory()
    :type max_step: np.array (size 6)

    :return: number of steps into which each interval is discretized
    :rtype: list [ , , ...]
    """
    assert trajectory.name == "souhaitee"

    def calcul_nb_steps_interval(trajectory, j):
        """
        For one interval, gives the number of steps to do for one interval.
        At first, we compute the number of steps needed for each dimension
        (x, y, z, alpha, beta, gamma); then we take the maximum of these values
        and we round it to the next integer.
        """
        nb_steps_dim = []
        for dim in range(6):
            nb_steps_dim.append(abs(trajectory.array[j+1][dim] -
                                    trajectory.array[j][dim]) / max_step[dim])
        return math.ceil(max(nb_steps_dim))

    nb_interval = len(trajectory.array) - 1
    nb_steps = []
    for j in range(nb_interval):
        nb_steps.append(calcul_nb_steps_interval(trajectory, j))

    assert len(trajectory.array) - 1 == len(nb_steps)
    return nb_steps


def discretize_traj(trajectory, max_step):
    """
    Discretize the trajectory by cutting intervals into constant valued steps,
    of value inferior to max_step.
    Return 2 lists:
    1. the list of the points in space (6D) we have to go through. It is
    useless for the motors but it will be useful to plot the trajectory;
    2. the list of the infinitesimal moves we need to do to go from a point to
    another.

    :param trajectory: trajectory we want the mobile to follow
    :param max_step: maximal step for each dimension

    :type trajectory: Trajectory()
    :type max_step: np.array (size 6)

    :return: points we have to go through; infinitesimal moves
    :rtype: (list, list)
    """
    nb_steps = calcul_nb_steps(trajectory, max_step)
    nb_interval = len(trajectory.array) - 1

    traj_disc = []
    var_disc = []
    for j in range(nb_interval):
        # for each interval between 2 points of the trajectory
        dx = trajectory.dx(nb_steps, j)
        dy = trajectory.dy(nb_steps, j)
        dz = trajectory.dz(nb_steps, j)
        da = trajectory.da(nb_steps, j)
        db = trajectory.db(nb_steps, j)
        dg = trajectory.dg(nb_steps, j)

        for i in range(0, nb_steps[j]):
            # for each step
            x = trajectory.array[j][0] + i * dx
            y = trajectory.array[j][1] + i * dy
            z = trajectory.array[j][2] + i * dz
            a = trajectory.array[j][3] + i * da
            b = trajectory.array[j][4] + i * db
            g = trajectory.array[j][5] + i * dg

            traj_disc.append([x, y, z, a, b, g])
            var_disc.append([dx, dy, dz, da, db, dg])

    return np.array(traj_disc), np.array(var_disc)


# 2. LONGUEUR DES CABLES

def pos_to_cable_length(position):
    """
    cf calcul_longueurs_cables

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
    pass


def get_cable_var(mobile, trajectory_disc, dimensions):
    """
    cf commande_longieurs_cables

    Convertit la trajectory discrétisée (liste des déplacements infinitésimaux
    qu'il faut réaliser pour parcourir la trajectory souhaitée) en la liste
    des modifications infinitésimales des longueurs des câbles et la liste des
    longueurs des cordes.

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


    :param traj_disc: trajectory discrétisée dans la première partie du code,
    chaque point de la trajectory est un np.array de taille 6.
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

    USING: - pos_to_cable_length
    """
    pass


def display_pas():
    for dim in range(6):
        print("Pas de %s %s : %.3f %s" % (typedim[dim//3],
                                          dim6d[dim],
                                          max_step[dim],
                                          units[dim//3]
                                          ))


# MAIN #

def main():
    # trajectory
    trajectory = obj.Trajectory("souhaitee", array_trajectory)
    traj_disc = obj.Trajectory("discretisee", discretize_traj(trajectory, max_step)[0])


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("\n*** End ***\n"
          "Start: {0}\n"
          "End: {1}\n"
          "Time Elapsed: {2:.2f}s".format(
            time.strftime("%Hh%Mm%Ss", time.localtime(start_time)),
            time.strftime("%Hh%Mm%Ss", time.localtime(end_time)),
            end_time - start_time))
