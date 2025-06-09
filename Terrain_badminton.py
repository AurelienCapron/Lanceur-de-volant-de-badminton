"""
Nom du fichier : Terrain_badminton.py
Auteur : CAPRON Aurélien
Date : 12/02/2025
Description :
    Ce script génère une représentation graphique d'un terrain de badminton avec des 
    éléments interactifs tels que les lignes du terrain, la position des caméras et du 
    lanceur, la portée des capteurs, la position du joueur et les zones de difficulté.
"""

import cv2
import numpy as np
from Variables_positions import player_on_court, position_on_court, dimension_scale, dimension_representation, position_launcher, position_cameras

#--------- Convertion des dimensions réelles en pixels ---------

scale = dimension_scale()

position_launcher_court = position_on_court(dimension_representation[0],dimension_representation[1],position_launcher[1],position_launcher[0])
position_cameras_court = position_on_court(dimension_representation[0],dimension_representation[1],position_cameras[1],position_cameras[0])

thickness_lines = int(40/scale)

service_lines = int(1980/scale)
corridor_back = int(720/scale)
corridor_side = int(420/scale)

# =========================================================================================== #
#                                1. Dessin des lignes du terrain                              #
# =========================================================================================== #

def dotted_lines(img):
    """
    But : Tracer le filet sous forme de ligne pointillée.

    Méthode : La fonction crée une ligne en alternant des segments pleins (dash_length) et des espaces vides (gap_length).
    """
    height, width, _ = img.shape
    center_h = int(height/2)  # Calcul du centre en hauteur

    dash_length = 25
    gap_length = 23

    start_point = (0, center_h)
    end_point = (width, center_h)
    line_length = int(np.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1]))

    for i in range(0, line_length, dash_length + gap_length):
        x_start = int(start_point[0] + (i / line_length) * (end_point[0] - start_point[0]))
        y_start = int(start_point[1] + (i / line_length) * (end_point[1] - start_point[1]))

        x_end = int(start_point[0] + ((i + dash_length) / line_length) * (end_point[0] - start_point[0]))
        y_end = int(start_point[1] + ((i + dash_length) / line_length) * (end_point[1] - start_point[1]))

        cv2.line(img, (x_start, y_start), (x_end, y_end), (255,255,255), thickness_lines)

def lines(img):
    """
    But : Tracer les lignes principales du terrain de badminton.

    Méthode : Utilisation de cv2.line() pour dessiner les contours et les lignes de service.
    """
    height, width, _ = img.shape

    # Calcul des centres en hauteur et largeur
    center_h = int(height/2)
    center_w = int(width/2)

    white = (255,255,255)

    # Lignes haut/bas
    cv2.line(img,(0,0),(width,0),white,thickness_lines)
    cv2.line(img,(0,height),(width,height),white,thickness_lines)

    # Lignes gauche/droite
    cv2.line(img,(0,0),(0,height),white,thickness_lines)
    cv2.line(img,(width,0),(width,height),white,thickness_lines)

    # Lignes de service
    cv2.line(img,(0,center_h+service_lines),(width,center_h+service_lines),white,thickness_lines)
    cv2.line(img,(0,center_h-service_lines),(width,center_h-service_lines),white,thickness_lines)

    # Lignes des couloirs arrières
    cv2.line(img,(0,corridor_back),(width,corridor_back),white,thickness_lines)
    cv2.line(img,(0,height-corridor_back),(width,height-corridor_back),white,thickness_lines)

    # Lignes des couloirs de côté
    cv2.line(img,(corridor_side,0),(corridor_side,height),white,thickness_lines)
    cv2.line(img,(width-corridor_side,0),(width-corridor_side,height),white,thickness_lines)

    # Lignes de côté
    cv2.line(img,(center_w,0),(center_w,center_h-service_lines),white,thickness_lines)
    cv2.line(img,(center_w,center_h+service_lines),(center_w,height),white,thickness_lines)

    # Filet
    dotted_lines(img)

# =========================================================================================== #
#                             2. Affichage des éléments du terrain                            #
# =========================================================================================== #

def launcher(img,position_launcher_court,color):
    """
    But : Afficher une représentation du lanceur.

    Méthode : Dessin d'un rectangle à la position du lanceur.
    """
    rect_height = 30
    rect_width = 30

    #print("launcheur :",position_launcher_court)
    #print((int(position_launcher_court[0]-rect_width/2),int(position_launcher_court[1]-rect_height/2)))

    point_bottom_left = (int(position_launcher_court[0]-rect_width/2),int(position_launcher_court[1]-rect_height/2))
    point_top_right = (int(position_launcher_court[0]+rect_width/2),int(position_launcher_court[1]+rect_height/2))

    cv2.rectangle(img,point_bottom_left,point_top_right,color,-1)

def cameras(img,position_cameras_court,baseline,color):
    """
    But : Afficher les caméras sur le terrain.

    Méthode : Dessin de cercles aux positions des caméras.
    """
    radius = 15

    #print((int((position_cameras_court[0]-baseline)/2),position_cameras_court[1]))

    cv2.circle(img,(int((position_cameras_court[0]-baseline)/2),position_cameras_court[1]),radius,color,-1)
    cv2.circle(img,(int((position_cameras_court[0]+baseline)/2),position_cameras_court[1]),radius,color,-1)

def camera_fov(img,position_cameras_court,baseline,fov_left,fov_right,color):
    """
    But : Afficher le champ de vision des caméras sous forme de lignes de perspective.

    Méthode : Calcul des angles de vision et tracé des lignes.
    """
    position_camera_left = (int((position_cameras_court[0]-baseline)/2),position_cameras_court[1])
    position_camera_right = (int((position_cameras_court[0]+baseline)/2),position_cameras_court[1])

    x_left = int(position_cameras_court[1]*np.tan(fov_left/2))
    x_right = int(position_cameras_court[1]*np.tan(fov_right/2))

    cv2.line(img,position_camera_left,(position_camera_left[0]-x_left,0),color,thickness_lines)
    cv2.line(img,position_camera_left,(position_camera_left[0]+x_left,0),color,thickness_lines)

    cv2.line(img,position_camera_right,(position_camera_right[0]-x_right,0),color,thickness_lines)
    cv2.line(img,position_camera_right,(position_camera_right[0]+x_right,0),color,thickness_lines)

def scope_of_action(img,position_launcher_court,scope_launcher,color):
    """
    But : Représenter l'angle d'action du lanceur.
    """
    x = int(position_launcher[1]/np.tan(scope_launcher/2))

    cv2.line(img,position_launcher_court,(position_launcher_court[0]-x,0),color,thickness_lines)
    cv2.line(img,position_launcher_court,(position_launcher_court[0]+x,0),color,thickness_lines)

# =========================================================================================== #
#                               3. Suivi et affichage du joueur                               #
# =========================================================================================== #

#--------- Affichage du joueur et de la difficulté  ---------

def player(img,position,color):
    """
    But : Afficher la position du joueur sous forme d'un cercle.
    """
    radius = 20

    cv2.circle(img,position,radius,color,-1)

def difficulty(img,radius,position,position_difficulty,color):
    """
    But : Visualiser le rayon et la position de la difficulté sous forme d'un cercle.
    """
    radius_position_difficulty = 10

    cv2.circle(img,position,radius,color,thickness_lines)
    cv2.circle(img,position_difficulty,radius_position_difficulty,color,-1)

def permanent(img,position,color):
    """
    But : Afficher la position de tir permanente sous forme d'un cercle.
    """
    radius = 10

    cv2.circle(img,position,radius,color,-1)

#--------- Lignes reliant le joueur aux caméras et au lanceur ---------

def player_cameras(img,position,baseline,color):
    """
    But : Montrer la connexion entre le joueur et les caméras.
    """
    height, width, _ = img.shape 

    cv2.line(img,position,(int((width-baseline)/2),height),color,thickness_lines)
    cv2.line(img,position,(int((width+baseline)/2),height),color,thickness_lines)

def player_launcher(img,position,color):
    """
    But : Afficher une ligne reliant le joueur au lanceur.
    """
    height, width, _ = img.shape 
    center_w = int(width/2)  # Calcul du centre en largeur
    
    cv2.line(img,position,(center_w,height),color,thickness_lines)

#--------- Lignes schématisant la hauteur et largeur du joueur ---------

def player_height(img,position,color):
    """
    But : Visualiser la hauteur du joueur sur le terrain.
    """
    height = img.shape[0]

    cv2.line(img,position,(position[0],height),color,thickness_lines)

def player_width(img,position,color):
    """
    But : Visualiser la largeur du joueur sur le terrain.
    """
    width= img.shape[1]

    cv2.line(img,(int(width/2),position[1]),position,color,thickness_lines)

#--------- Affichage des angles ---------

def angle_cameras(img,position_cameras_court,baseline,angle_left,angle_right,color):
    """
    But : Visualiser l'angle entre le joueur et les caméras.
    """
    radius = 40

    cv2.ellipse(img,(int((position_cameras_court[0]-baseline)/2),position_cameras_court[1]),(radius, radius),0,180,180+np.degrees(angle_left),color,thickness_lines)
    cv2.ellipse(img,(int((position_cameras_court[0]+baseline)/2),position_cameras_court[1]),(radius, radius),0,180,180+np.degrees(angle_right),color,thickness_lines)

def angle_launcher(img,position_launcher_court,angle,radius,color):
    """
    But : Visualiser l'angle entre le joueur et le lanceur.
    """

    cv2.ellipse(img,(position_launcher_court[0],position_launcher_court[1]),(radius, radius),0,270,270+np.degrees(angle),color,thickness_lines)

#--------- Affichage des dimensions réelles du joueur sous forme de texte ---------

def text_height_width(img,position,depth_player,width_player,color):
    """
    But : Afficher la profondeur et la largeur réelle du joueur.
    """
    height, width, _ = img.shape 
    fontFace = 1
    fontScale = 2
    thickness = 2
    
    cv2.putText(img,f"{round(width_player)}mm",(abs(int(((width/2)+position[0])/2)),position[1]-10),fontFace,fontScale,color,thickness)
    cv2.putText(img,f"{round(depth_player)}mm",(position[0]+10,position[1]+int((height-position[1])/2)),fontFace,fontScale,color,thickness)

def text_angle_camera(img,position_cameras_court,baseline,angle_left,angle_right,color):
    """
    But : Afficher l'angle entre le joueur et les caméras.
    """
    fontFace = 1
    fontScale = 2
    thickness = 2

    angle_left = round(np.degrees(angle_left))
    angle_right = round(np.degrees(angle_right))

    cv2.putText(img,f"{angle_left}deg",(int((position_cameras_court[0]-baseline)/2)-165,position_cameras_court[1]-10),fontFace,fontScale,color,thickness)
    cv2.putText(img,f"{angle_right}deg",(int((position_cameras_court[0]+baseline)/2)+30,position_cameras_court[1]-10),fontFace,fontScale,color,thickness)

def text_angle_launcher(img,position_launcher_court,angle_player,angle_difficulty,color_player,color_difficulty):
    """
    But : Afficher l'angle entre le joueur et le lanceur.
    """
    fontFace = 1
    fontScale = 2
    thickness = 2

    angle_player = round(np.degrees(angle_player))
    angle_difficulty = round(np.degrees(angle_difficulty))

    cv2.putText(img,f"{angle_player}deg",(position_launcher_court[0]-120,position_launcher_court[1]-50),fontFace,fontScale,color_player,thickness)
    cv2.putText(img,f"{angle_difficulty}deg",(position_launcher_court[0]-120,position_launcher_court[1]-10),fontFace,fontScale,color_difficulty,thickness)

# =========================================================================================== #
#                               4. Génération et affichage final                              #
# =========================================================================================== #

def badminton_court(baseline,scope_launcher,fov_left,fov_right,color_court,color_launcher,color_camera,display):
    """
    Génère une représentation visuelle d'un terrain de badminton.
    """
    print("launcheur :",position_launcher,position_launcher_court)
    print("cameras :",position_cameras,position_cameras_court)
    # Création d'une image remplie avec la couleur du terrain
    court = np.full(dimension_representation,color_court,dtype=np.uint8)

    # Si display est une liste contenant uniquement [True], on l'étend pour afficher tous les éléments
    if display == [True] : 
        display *= 5  # On duplique pour couvrir tous les éléments possibles
    
    # Vérifie si au moins un élément doit être affiché
    if set(display) != {False}:
        if display[0]:  # Affichage des lignes du terrain
            lines(court)
        if display[1]:  # Affichage du lanceur
            launcher(court,position_launcher_court,color_launcher)
        if display[2]:  # Affichage du champ d’action du lanceur
            scope_of_action(court,position_launcher_court,scope_launcher,color_launcher)
        if display[3]:  # Affichage des caméras
            cameras(court,position_cameras_court,baseline,color_camera)
        if display[4]:  # Affichage du champ de vision des caméras
            camera_fov(court,position_cameras_court,baseline,fov_left,fov_right,color_camera)
        return court

def representation(court,baseline,position_court,position_court_reality,depth_player,width_player,total_angle_left,total_angle_right,angle_player_launcher,radius_difficulty,position_difficulty_reality,position_difficulty_court,angle_difficulty,permanent_position_court,color_player_width_height,color_difficulty,color_launcher,color_camera,color_player2camera,color_angle_camera,color_player2launcher,color_angle_launcher,display):
    """
    Ajoute les différents éléments visuels liés au joueur et aux caméras sur la représentation du terrain de badminton.
    """
    # Copie de l'image du terrain pour modifications
    court_mod = np.copy(court)

    # Si display est une liste contenant uniquement [True], on l'étend pour afficher tous les éléments
    if display == [True] : 
        display *= 7  # On duplique pour couvrir tous les éléments possibles

    # Vérifie si au moins un élément doit être affiché et si le joueur est sur le terrain
    if set(display) != {False} and player_on_court(court, position_court[1], position_court[0]):
        # Affichage de l'angle entre le joueur et le lanceur ainsi que l'angle de difficulté
        text_angle_launcher(court_mod,position_launcher_court,angle_player_launcher,angle_difficulty,color_angle_launcher,color_difficulty)

        # Affichage des interactions avec les caméras
        if display[0]:
            angle_cameras(court_mod,position_cameras_court,baseline,total_angle_left,total_angle_right,color_angle_camera) 
            player_cameras(court_mod,position_court,baseline,color_player2camera)
            text_angle_camera(court_mod,position_cameras_court,baseline,total_angle_left,total_angle_right,color_angle_camera)

        # Affichage des interactions avec le lanceur
        if display[1]:
            if position_court_reality[0] > 250:
                angle_launcher(court_mod,position_launcher_court,angle_player_launcher,250,color_angle_launcher)
            else:
                angle_launcher(court_mod,position_launcher_court,angle_player_launcher,int(position_court_reality[0]*3/4),color_angle_launcher)
            player_launcher(court_mod,position_court,color_player2launcher)

        # Affichage de la difficulté et de son angle
        if display[2]:
            if position_difficulty_reality[0] > 260:
                angle_launcher(court_mod,position_launcher_court,angle_difficulty,260,color_difficulty)
            else:
                angle_launcher(court_mod,position_launcher_court,angle_difficulty,int(position_difficulty_reality[0]*3/4),color_difficulty)
            player_launcher(court_mod,position_difficulty_court,color_difficulty)

        # Affichage des dimensions du joueur (hauteur et largeur)
        if display[3]:
            player_height(court_mod,position_court,color_player_width_height)
            player_width(court_mod,position_court,color_player_width_height)
            text_height_width(court_mod,position_court,depth_player,width_player,color_player_width_height)

        # Affichage du joueur sur le terrain
        if display[4]:
            player(court_mod,position_court,color_player2camera)

        # Affichage de la zone de difficulté
        if display[5]:
            difficulty(court_mod,radius_difficulty,position_court,position_difficulty_court,color_difficulty)

        # Affichage de la position de tir permanante
        if display[6]:
            permanent(court_mod,permanent_position_court,color_player2camera)
    
    # Ajout des caméras et du lanceur sur le terrain
    cameras(court_mod,position_cameras_court,baseline,color_camera)
    launcher(court,position_launcher_court,color_launcher)

    return court_mod