"""
Nom du fichier : Programme_principale.py
Auteur : CAPRON Aurélien
Date : 24/01/2025
Description :
    Ce script constitue le script principal permettant :
    - l'affichage de la détection du joueur grâce à un filtre de couleur,
    - l'affichage de la position du joueur sur un terrain de badminton fictif,
    - l'envoi et la réception d'informations vers l'Arduino.
"""

# =========================================================================================== #
#                               1. Importation des bibliothèques                              #
# =========================================================================================== #

import cv2
import numpy as np
from Texte_image import image_display
from Detection_joueur import final_frame
from Determination_filtre import filter_determination
from Transfert_donnees_lanceur import connection_port, connexion_successful
from Terrain_badminton import badminton_court, representation, dimension_scale
from Variables_positions import player_variable, difficulty_variable, permanent_variable, field_of_view
from Interface_utilisateur import ModifiedParameter, input_analysis, difficulty_choice

# =========================================================================================== #
#                        2. Configuration des caméras et du port série                        #
# =========================================================================================== #

#--------- Configuration des caméras ---------
cap_left = cv2.VideoCapture(1)
cap_right = cv2.VideoCapture(0)

camera_left = "iPhone"   # Nom de caméra gauche
camera_right = "Webcam"  # Nom de caméra droite

problem_camera = False   # Variable indiquant le bon fonctionnement des caméras

#--------- Configuration du port série pour la communication Arduino ---------
port_usb = "/dev/cu.usbserial-140"  # Nom du port série
baudrate = 115200                   # Vitesse de communication en bauds

connexion_usb = connection_port(port_usb)  # On vérifie si le port série est disponible, sinon on envoie tous les ports disponibles
if connexion_usb:   
    ser = connexion_successful(port_usb,baudrate)  # Tentative de connexion au port USB. En cas d'échec, l'erreur associée est renvoyée.

# =========================================================================================== #
#                     3. Caractéristiques de l'installation caméra/lanceur                    #
# =========================================================================================== #

# Échelle de dimension entre le terrain réel et le terrain fictif
scale = dimension_scale()

# Distance réelle entre les deux caméras (en mm) et conversion selon l'échelle du terrain
baseline = 720
baseline_court = int(baseline/scale)

#--------- Détermination du champ de vision des caméras ---------
distance_iPhone2screen = [1.122,1.421,1.834]  # Distances entre l'iPhone et l'écran (en m)
length_screen_iPhone = [1.462,1.834,2.346]    # Largeurs de l'écran pour l'iPhone (en m)

distance_webcam2screen = [1.016,1.313,1.994]  # Distances entre la webcam et l'écran (en m)
length_screen_webcam = [1.375,1.777,2.678]    # Largeurs de l'écran pour la webcam (en m)

# Calcul du champ de vision pour chaque caméra
vision_field_left = field_of_view(distance_iPhone2screen,length_screen_iPhone)
vision_field_right = field_of_view(distance_webcam2screen,length_screen_webcam)

# Définition du champ d'action du lanceur
scope_launcher = np.pi/2

#--------- Détermination des filtres de couleur ---------

# Détermination des filtres de couleur pour chaque caméra
low_color_left, high_color_left = filter_determination(cap_left, camera_left)
low_color_right, high_color_right = filter_determination(cap_right, camera_right)

# =========================================================================================== #
#                             4. Paramétrage des affichages écran                             #
# =========================================================================================== #

#--------- Affichage des caméras ---------
only_player_detection = True  # Active l'affichage du joueur uniquement. Si False, affiche aussi les formes rouges.
text_display = [True]         # Active l'affichage des données du joueur avec des paramètres spécifiques : position de la caméra, profondeur, largeur, angle de la caméra, angle total et angle du lanceur.
text_color = (0,0,255)        # Couleur du texte affiché
fontFace = 1                  # Police du texte
fontScale = 2                 # Taille du texte
thickness = 2                 # Épaisseur du texte

#--------- Initialisation du terrrain de badminton ---------
court_initialization_display = [True]  # Initialisation du terrain de badminton avec des paramètres spécifiques : lignes, lanceur, champ d'action du lanceur, caméras et champs de vision des caméras.
color_court = (183,107,0)              # Couleur du terrain
color_launcher = (0,255,255)           # Couleur du lanceur
color_camera = (0,0,255)               # Couleur des caméras

#--------- Affichage joueur/difficulté sur le terrain ---------
court_display = [True]                   # Active l'affichage du joueur sur le terrain avec des paramètres spécifiques : joueur/caméras, joueur/lanceur, difficulté/lanceur, profondeur et largeur, joueur, difficulté.
color_difficulty = (200,200,200)         # Couleur de la difficulté
color_player_width_height = (255,0,147)  # Couleur de la largeur/profondeur du joueur
color_player2camera = (255,0,0)          # Couleur des lignes joueur/caméras
color_player2launcher = (255,255,0)      # Couleur des lignes joueur/lanceur
color_angle_camera = (0,255,0)           # Couleur des angles totaux
color_angle_launcher = (255,255,0)       # Couleur de l'angle avec le lanceur

# =========================================================================================== #
#     5. Initialisation des paramètres du mode suivi du joueur et du niveau de difficulté     #
# =========================================================================================== #

difficulty_choice()  # On informe l'utilisateur des différents niveaux de difficulté ainsi que le moyen de changer dynamiquement certains paramètres

parameter = ModifiedParameter()  # Création d'une instance de la classe

#--------- Mise à jour dynamique des variables sur Arduino ---------

level_difficulty = 1  # Niveau de difficulté

#--------- Mise à jour dynamique des variables sur la console Python ---------

camera_display = True                 # Initialisation d'un drapeau pour l'initialisation des images à afficher

selected_frame = "Sans modification"  # Initialisation du variable pour le changement d'affichage caméra

tracking_mode = str(False)            # Mode de suivi du joueur

position_permanent = [3000,0]         # Position du tir de volant bloqué (en mm) : [profondeur,largeur]

radius_difficulty = 1000              # Rayon de la difficulté (en mm)

frequency_throw = 0                   # Fréquence de lancement des volants

frequency_launcher = 1000             # Fréquence de mise à jour du lanceur

#--------- Variables temporaires ---------
altitude = 0
puissance = 0
# TODO : Faire une fonction qui à l'aide des équations du volant renvoie une altitude et une puissance à envoyer à l'arduino

# =========================================================================================== #
#                                     6. Boucle principale                                    #
# =========================================================================================== #

# Création du terrain fictif
court = badminton_court(baseline_court,scope_launcher,vision_field_left,vision_field_right,color_court,color_launcher,color_camera,court_initialization_display)

real_condition_launcher = False  # Condition réel de l'utilisation du lanceur

previous_written_value = 0  # Initialisation de la variable pour stocker la dernière valeur écrite et détecter les changements

while True:

    # Capture des images des caméras
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    # Vérification que les deux caméras fonctionnent correctement
    if not ret_left or not ret_right:
        problem_camera = True
        print("\n\033[31mProblème lors de la connexion aux caméras\033[0m\n")
        break

    # Ajustement du rayon de difficulté en fonction de l'échelle du terrain
    radius_difficulty_court = int(radius_difficulty/scale)
    
    # Détection du joueur sur chaque caméra
    frame_figure_left, threshold_left, threshold_figure_left, color_left, color_figure_left, position_left = final_frame(frame_left,low_color_left,high_color_left,only_player_detection)
    frame_figure_right, threshold_right, threshold_figure_right, color_right, color_figure_right, position_right = final_frame(frame_right,low_color_right,high_color_right,only_player_detection)

    # Calcul de la position du joueur et des angles réels
    depth_player,width_player,angle_left,angle_right,total_angle_left,total_angle_right,azimut = player_variable(color_figure_left,baseline,position_left,position_right,vision_field_left,vision_field_right)
    
    # Détermination de la position du joueur et de la difficulté sur le terrain fictif ainsi que l'azimut de la difficulté
    position_player_court, position_player_court_base, position_difficulty_court, position_difficulty_base, azimut_difficulty = difficulty_variable(court,depth_player,width_player,level_difficulty,radius_difficulty_court,real_condition_launcher)

    # Détermination de la position de la position de tir permanent sur le terrain fictif ainsi que son azimut
    position_permanent_court, position_permanent_court_base, azimut_permanent = permanent_variable(court,position_permanent)

    #--------- Affichage des caméras et du terrain fictif ---------

    # Initialisation des images des caméras à afficher
    if camera_display:
        selected_frame_left = frame_figure_left
        selected_frame_right = frame_figure_right
        camera_display = False

    # Application du texte sur chaque frame
    final_frame_left = image_display(selected_frame_left,depth_player,width_player,position_left,angle_left,total_angle_left,azimut,fontFace,fontScale,text_color,thickness,text_display,"Camera Gauche")
    final_frame_right = image_display(selected_frame_right,depth_player,width_player,position_right,angle_right,total_angle_right,azimut,fontFace,fontScale,text_color,thickness,text_display,"Camera Droite")

    # Application des paramètres sur le terrain fictif
    final_court = representation(court,baseline_court,position_player_court,position_player_court_base,depth_player,width_player,total_angle_left,total_angle_right,azimut,radius_difficulty_court,position_difficulty_base,position_difficulty_court,azimut_difficulty,position_permanent_court,color_player_width_height,color_difficulty,color_launcher,color_camera,color_player2camera,color_angle_camera,color_player2launcher,color_angle_launcher,court_display)

    # On combine les deux images et le terrain dans une seule image
    combined = cv2.hconcat([final_court,cv2.vconcat([final_frame_left, final_frame_right])])

    # On affiche l'image créée
    cv2.imshow("Position du joueur", combined)

    #--------- Envoi des données à l'Arduino ---------

    # Vérification si la connexion USB est établie
    if connexion_usb:

        # On envoie les paramètres au lanceur en fonction de l'activation du mode de suivi du joueur
        if tracking_mode in ["True","true"]:
            azimut_servo = round(np.degrees(azimut_difficulty))
        else:
            azimut_servo = round(np.degrees(azimut_permanent))

        # Envoi des données au microcontrôleur via le port série. Format des données envoyées : "azimut:altitude:puissance:fréquence:difficulté"
        ser.write((f"{azimut_servo}:{altitude}:{puissance}:{frequency_throw}:{frequency_launcher}:{level_difficulty}\n").encode())

        # Vérification si des données sont disponibles en retour depuis l'Arduino
        if ser.in_waiting > 0:
            level = (ser.readline().decode("utf-8").strip()) # Lecture et décodage des données reçues

            # Mise à jour du niveau de difficulté uniquement si la valeur reçue est différente de la valeur actuelle et si elle correspond à un niveau valide (1, 2 ou 3)
            if (level != f"{level_difficulty}") and (level in ["1","2","3"]):
                level_difficulty = int(level)

    #--------- Mise à jour de différents paramètres ---------

    # Récupération de la valeur modifiée de la difficulté par l'utilisateur
    written_value = parameter.valeur_modifiee

    # Analyse de l'entrée utilisateur pour déterminer s'il s'agit d'une fréquence ou d'un rayon de difficulté
    modified_value , written_value = input_analysis(written_value)
    
    index_modification = str(modified_value) + str(written_value)

    # On vérifie que la valeur écrite est différente de la précédente
    if index_modification != previous_written_value:

        # Mise à jour des paramètres en fonction du type de valeur écrite

        # Mise à jour du mode de suivi
        if modified_value == 1:
            tracking_mode = written_value
            if tracking_mode in ["True","true"]:
                print("\033[32mActivation du mode de suivi du joueur\033[0m\n")
            else:
                print("\033[31mDésativation du mode de suivi du joueur\033[0m\n")

        # Mise de l'affichage des caméras
        elif modified_value == 2: 
            if written_value == "1":
                selected_frame = "Sans modification"
                print(f"\033[36mAffichage modifiée à : sans modification\033[0m\n")
            elif written_value == "2":
                selected_frame = "Seuillage"
                print(f"\033[36mAffichage modifiée à : seuillage\033[0m\n")
            else:
                selected_frame = "Couleur filtrée"
                print(f"\033[36mAffichage modifiée à : couleur filtrée\033[0m\n")

        # Mise à jour de la fréquence d'envoi du volant
        elif modified_value == 3:
            frequency_throw = written_value
            print(f"\033[34mModification de la fréquence d'envoi des volants à {frequency_throw}ms\033[0m\n")

        # Mise à jour de la fréquence de mise à jour du lanceur
        elif modified_value == 4:
            frequency_launcher = written_value
            print(f"\033[34mModification de la fréquence de mise à jour du lanceur à {frequency_launcher}ms\033[0m\n")

        # Mise à jour du rayon de difficulté
        elif modified_value == 5:
            radius_difficulty = written_value
            print(f"\033[34mModification du rayon de difficulté à {radius_difficulty}mm\033[0m\n")

        # Mise à jour de la profondeur de la position permanente de tir
        elif modified_value == 6:
            position_permanent[0] = written_value
            print(f"\033[34mModification de la profondeur de la position permanente de tir à {position_permanent[0]}mm\033[0m\n")

        # Mise à jour de la largeur de la position permanente de tir
        elif modified_value == 7:
            position_permanent[1] = written_value
            print(f"\033[34mModification de la largeur de la position permanente de tir à {position_permanent[1]}mm\033[0m\n")

        previous_written_value = index_modification

    if selected_frame == "Sans modification":
        selected_frame_left, selected_frame_right = frame_figure_left, frame_figure_right
    elif selected_frame == "Seuillage":
        selected_frame_left, selected_frame_right = threshold_figure_left, threshold_figure_right
    elif selected_frame == "Couleur filtrée":
        selected_frame_left, selected_frame_right = color_figure_left, color_figure_right
    
    # Vérifie si l'utilisateur appuie sur la touche 'Échap' pour quitter la boucle principale
    if cv2.waitKey(1) == 27:
        break

# =========================================================================================== #
#                          7. Libération du port série et des caméras                         #
# =========================================================================================== #

if connexion_usb:
    ser.close()
    print(f"Fermeture du port \033[34m{port_usb}\033[0m")

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()

if not problem_camera:
    print(f'Libération des caméras \033[1mGauche\033[0m : \033[36m"{camera_left}"\033[0m et \033[1mDroite\033[0m : \033[36m"{camera_right}"\033[0m\n')