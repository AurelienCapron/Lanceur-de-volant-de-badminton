"""
Nom du fichier : Variables_positions.py
Auteur : CAPRON Aurélien
Date : 14/02/2025
Description :
    Ce script contient des fonctions permettant de calculer diverses variables relatives à un joueur sur un terrain de badminton,
    comme la profondeur, la largeur, l'angle de la caméra, et la position du joueur. Il inclut aussi des calculs pour la difficulté du jeu
    et la projection de la position du joueur sur le terrain en fonction de la vision de la caméra et d'autres paramètres.
"""

import numpy as np
from random import uniform
from math import sqrt

dimension_real = (13400,6100,3)          # Dimensions réelles du terrain (en mm)
dimension_representation = (2160,984,3)  # Dimensions de l'image de représentation (en pixels), la hauteur est déterminée par la hauteur de deux images de taille (1080, 1920, 3)

def dimension_scale():
    """
    Calcule le facteur d'échelle entre les dimensions réelles et les dimensions représentées du terrain.

    L'échelle est obtenue en divisant la première dimension réelle du terrain 
    par la première dimension de sa représentation fictive.
    """
    return dimension_real[0]/dimension_representation[0]

def random_point_circle(depth, width, level, radius):
    """
    But : Générer un point aléatoire à l'intérieur d’un cercle pour simuler la dispersion des tirs.
    """
    # Génération d'un rayon aléatoire avec une distribution uniforme
    if level == 2:
        radius = radius * sqrt(uniform(0, 1))
    
    # Génération d'un angle aléatoire entre 0 et 2π
    random_angle = uniform(0, 2 * np.pi)
    
    # Conversion en coordonnées cartésiennes
    x = width + radius * np.cos(random_angle)
    y = depth + radius * np.sin(random_angle)
    
    return int(x), int(y)

# =========================================================================================== #
#                                 1. Caractéristiques des caméras                             #
# =========================================================================================== #

def field_of_view(distance_camera_screen,screen_length):
    """
    Calcule l'angle de champ de vision (FOV) moyen d'une caméra en fonction des distances de caméra et des longueurs d'écran.
    """
    n = len(distance_camera_screen)
    FOV = []
    for i in range(n):
        # Calcul de l'angle FOV pour chaque distance et longueur d'écran
        FOV.append(2*np.atan(screen_length[i]/(2*distance_camera_screen[i])))
    return np.average(FOV)  # Retourne la moyenne des angles FOV

def focal_length(frame,vision_field):
    """
    Calcule la distance focale d'une caméra à partir de la largeur de l'écran et de son champ de vision.
    """
    focal_length = frame.shape[1]/(2 * np.tan(vision_field/2))
    return focal_length

# =========================================================================================== #
#                             2. Calculs des paramètres du joueur                             #
# =========================================================================================== #

#--------- Calculs des angles ---------

def angle_camera_player(frame,position,vision_field):
    """
    Calcule l'angle entre la caméra et un joueur basé sur sa position sur le cadre et l'angle de vision de la caméra.
    """
    focal = focal_length(frame,vision_field)
    width_frame = frame.shape[1]
    center_width_frame = width_frame/2
    x = position[0]

    # Calcul de l'angle basé sur la position relative du joueur par rapport au centre de l'image
    if position[0] < center_width_frame:
        return (vision_field/2)-np.atan((center_width_frame-x)/focal)
    else:
        return (vision_field/2)+np.atan((x-center_width_frame)/focal)

def angle_base_camera(vision_field):
    """
    Calcule l'angle de la caméra par rapport à l'axe de référence basé sur le champ de vision.
    """
    return (np.pi-vision_field)/2

def total_angle(angle_camera_player,angle_base_camera):
    """
    Calcule l'angle total entre la caméra et un joueur, en prenant en compte l'angle de la caméra et l'angle de base.
    """
    return angle_camera_player + angle_base_camera

def angle_position_launcher(depth_player,width_player):
    """
    Calcule l'azimut du joueur par rapport à la caméra (l'angle horizontal entre le joueur et la ligne de visée de la caméra).
    """
    if depth_player == 0 :
        return 0
    return np.atan(width_player/depth_player)

#--------- Calculs de la profondeur/largeur ---------

def depth(angle_left,angle_right,baseline):
    """
    Calcule la profondeur d'un joueur sur le terrain en utilisant les angles de caméra gauche et droite, ainsi que la distance de base entre les caméras.
    """
    tal = np.tan(angle_left)
    tar = np.tan(angle_right)

    return (baseline*tal*tar)/(tal-tar) 

def width(angle_left,angle_right,baseline):
    """
    Calcule la largeur du joueur (distance horizontale) à partir des angles de la caméra gauche et droite.
    """
    tal = np.tan(angle_left)
    bl = baseline/2
    d = depth(angle_left,angle_right,baseline)
    
    return -((d/tal)+bl)

# =========================================================================================== #
#                        3. Gestion des positions sur le terrain fictif                       #
# =========================================================================================== #

def player_on_court(frame, depth, width):
    """
    But : Vérifier si le joueur est situé à l'intérieur des limites du terrain.
    """
    height_frame, width_frame, _ = frame.shape

    return ((depth in range(0,height_frame)) and (width in range(0,width_frame)))

def position_on_court(img,depth_player,width_player):
    """
    But : Convertir la position réelle du joueur en pixels sur l’image de représentation.
    """
    height_img, width_img, _ = img.shape

    scale = dimension_scale()  # Calcul du facteur d'échelle pour conversion mm -> pixels
    depth_player = int(depth_player/scale)  # Conversion de la profondeur en pixels
    width_player = int(width_player/scale)  # Conversion de la largeur en pixels

    y = int(height_img - depth_player)  # Ajustement de la profondeur pour correspondre au repère de l'image

    # Calcul de la position horizontale du joueur en fonction du centre du terrain
    if width_player < 0:
        x = int((width_img/2) - abs(width_player))  # Joueur à gauche du centre
    else:
        x = int((width_img/2) + width_player)  # Joueur à droite du centre
    return x, y

def position_difficulty_on_court(frame, depth, width, level, radius, real_condition_launcher):
    """
    Détermine la position de la difficulté sur le terrain en fonction du niveau choisi.
    """
    height_frame, width_frame, _ = frame.shape
    center_h = int(height_frame/2)  # Calcul du centre en hauteur

    # Définition de la profondeur maximale selon la condition du lanceur
    if real_condition_launcher:
        depth_max = center_h - 1500  # Limite imposée par le lanceur
    else:
        depth_max = height_frame  # Pas de limite spécifique
    
    # Si le niveau de difficulté est 1, on garde la position initiale
    if level == 1:
        return width, depth 
    else :
        # Génération d'une position aléatoire dans un rayon autour de la position initiale
        x, y = random_point_circle(depth, width, level, radius)

        # Vérification que la position générée est bien dans les limites du terrain
        while (x not in range(0,width_frame)) or (y not in range(0,depth_max)):
            x, y = random_point_circle(depth, width, level, radius)

        return x, y

def position_court_base(img,position_on_court):
    """
    Convertit les cordonnées d'une position sur le terrain (en coordonnées de l'image) en position par rapport au repère créé par le lanceur (origine) et les deux caméras (abscisse).
    """
    height_img, width_img, _ = img.shape
    center_w = int(width_img/2)

    x = position_on_court[0] - center_w 
    y = int(height_img - position_on_court[1])

    return y, x
    
# =========================================================================================== #
#                         4. Centralisation des différentes variables                         #
# =========================================================================================== #

def player_variable(frame,baseline,position_left,position_right,vision_field_left,vision_field_right):
    """
    Calcule diverses variables du joueur (profondeur, largeur, angles) en fonction des positions des caméras et des champs de vision.
    """
    angle_bc_left = angle_base_camera(vision_field_left)
    angle_bc_right = angle_base_camera(vision_field_right)

    angle_left = angle_camera_player(frame,position_left,vision_field_left)
    angle_right = angle_camera_player(frame,position_right,vision_field_right)

    total_angle_left = total_angle(angle_left,angle_bc_left)
    total_angle_right = total_angle(angle_right,angle_bc_right)
    
    depth_player = depth(total_angle_left,total_angle_right,baseline)
    width_player = width(total_angle_left,total_angle_right,baseline) 

    azimut = angle_position_launcher(depth_player,width_player)

    return depth_player,width_player,angle_left,angle_right,total_angle_left,total_angle_right,azimut

def difficulty_variable(frame,depth_player,width_player,level_difficulty,radius_difficulty,real_condition_launcher):
    """
    Calcule les variables de difficulté en fonction de la position du joueur et des paramètres de difficulté du jeu.
    """
    position_player_court = position_on_court(frame,depth_player,width_player)
    position_player_court_base = position_player_court
    position_difficulty_court = position_player_court
    position_difficulty_base = position_player_court
    if player_on_court(frame, position_player_court[1], position_player_court[0]):
        position_player_court_base = position_court_base(frame,position_player_court)
        position_difficulty_court = position_difficulty_on_court(frame,position_player_court[1],position_player_court[0],level_difficulty,radius_difficulty,real_condition_launcher)
        position_difficulty_base = position_court_base(frame,position_difficulty_court)

    azimut_difficulty = angle_position_launcher(position_difficulty_base[0],position_difficulty_base[1])

    return position_player_court, position_player_court_base, position_difficulty_court, position_difficulty_base, azimut_difficulty

def permanent_variable(frame,position):
    """
    Calcule les variables de difficulté en fonction de la position du joueur et des paramètres de difficulté du jeu.
    """
    position_permanent_court = position_on_court(frame,position[0],position[1])
    position_permanent_court_base = position_court_base(frame,position_permanent_court)

    azimut_permanent = angle_position_launcher(position[0],position[1])

    return position_permanent_court, position_permanent_court_base, azimut_permanent