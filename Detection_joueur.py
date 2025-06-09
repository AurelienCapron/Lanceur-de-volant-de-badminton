"""
Nom du fichier : Detection_joueur.py
Auteur : CAPRON Aurélien
Date : 14/02/2025
Description :
    Ce script permet de détecter un joueur dans une image ou une vidéo en utilisant des filtres 
    de couleur et de seuillage, ainsi que des contours pour déterminer sa position sur le terrain.
"""

import cv2
import numpy as np

def red_filter(frame,low_color,high_color):
    """
    Applique un filtre de couleur pour détecter des objets dans une certaine plage.

    Paramètres :
    frame : np.ndarray
        Image d'entrée au format BGR.
    low_color : tuple (int, int, int)
        Valeurs HSV minimales pour la détection de la couleur rouge.
    high_color : tuple (int, int, int)
        Valeurs HSV maximales pour la détection de la couleur rouge.

    Retourne :
    np.ndarray
        Image filtrée où seules les zones de la couleur choisie sont conservées.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)          # Conversion en HSV
    color_mask = cv2.inRange(hsv_frame, low_color, high_color)  # Création du masque pour la couleur rouge
    color = cv2.bitwise_and(frame, frame, mask=color_mask)      # Application du masque sur l'image originale
    return color

def threshold_filter(frame):
    """
    Applique un seuillage binaire sur une image en niveaux de gris.

    Paramètres :
    frame : np.ndarray
        Image d'entrée au format BGR.

    Retourne :
    np.ndarray
        Image binaire après seuillage.
    """
    frame_gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # Conversion en niveaux de gris
    threshold = cv2.threshold(frame_gris,50,255,cv2.THRESH_BINARY)[1]  # Seuillage
    return threshold

def draw_figure_color(frame_ref,frame_mod):
    """
    Identifie le plus grand objet détecté (probablement le joueur) et dessine un rectangle et un point central autour de chaque objet de la couleur filtrée choisie détecté.

    Paramètres :
    frame_ref : np.ndarray
        Image de référence contenant les objets détectés (image seuillée).
    frame_mod : np.ndarray
        Image d'origine sur laquelle les figures seront dessinées.

    Retourne :
    tuple (np.ndarray, tuple (int, int))
        - Image avec les rectangles et points dessinés.
        - Coordonnées du centre de l'objet détecté.
    """
    contours = cv2.findContours(frame_ref,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]  # Détection des contours
    frame_final = np.copy(frame_mod)

    aire_max = 0  # Initialisation de la plus grande aire détectée
    rect_max = (0,0,0,0)  # Initialisation du plus grand rectangle détecté

    for cnt in contours :
        x,y,w,h = cv2.boundingRect(cnt)  # Définition du rectangle englobant
        if w*h > aire_max :  # Vérification si la zone est la plus grande trouvée
            aire_max = w*h
            rect_max=(x,y,w,h)

        cx = int((x + x + w) / 2)  # Calcul du centre en x
        cy = int((y + y + h) / 2)  # Calcul du centre en y

        # Dessin du rectangle et du point central
        cv2.rectangle(frame_final, (x,y), (x+w,y+h), (0, 255, 0), 2)
        cv2.circle(frame_final, (cx,cy), 5, (0, 255, 0), -1)

    x_max,y_max,w_max,h_max = rect_max  # Récupération des coordonnées du plus grand rectangle

    cx_max = int((x_max + x_max + w_max) / 2)  # Calcul du centre en x
    cy_max = int((y_max + y_max + h_max) / 2)  # Calcul du centre en y
        
    return frame_final, (cx_max,cy_max)

def draw_figure_player(frame_ref,frame_mod):
    """
    Identifie le plus grand objet détecté (probablement le joueur) et dessine un rectangle autour.

    Paramètres :
    frame_ref : np.ndarray
        Image de référence contenant les objets détectés (image seuillée).
    frame_mod : np.ndarray
        Image d'origine sur laquelle les figures seront dessinées.

    Retourne :
    tuple (np.ndarray, tuple (int, int))
        - Image avec le rectangle et le point central du joueur.
        - Coordonnées du centre du joueur détecté.
    """
    contours = cv2.findContours(frame_ref,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]  # Détection des contours
    frame_final = np.copy(frame_mod)
    
    aire_max = 0  # Initialisation de la plus grande aire détectée
    rect_max = (0,0,0,0)  # Initialisation du plus grand rectangle détecté

    for cnt in contours :
        x,y,w,h = cv2.boundingRect(cnt)  # Définition du rectangle englobant
        if w*h > aire_max :  # Vérification si la zone est la plus grande trouvée
            aire_max = w*h
            rect_max=(x,y,w,h)

    x,y,w,h = rect_max  # Récupération des coordonnées du plus grand rectangle

    cx = int((x + x + w) / 2)  # Calcul du centre en x
    cy = int((y + y + h) / 2)  # Calcul du centre en y

    # Dessin du rectangle et du point central
    cv2.rectangle(frame_final, (x,y), (x+w,y+h), (0, 255, 0), 2)
    cv2.circle(frame_final, (cx,cy), 5, (0, 255, 0), -1)

    return frame_final, (cx,cy)

def final_frame(frame,low_color,high_color,only_player_detection):
    """
    Traite une image pour détecter le joueur et les objets rouges.

    Paramètres :
    frame : np.ndarray
        Image d'entrée au format BGR.
    low_red : tuple (int, int, int)
        Valeurs HSV minimales pour la détection de la couleur rouge.
    high_red : tuple (int, int, int)
        Valeurs HSV maximales pour la détection de la couleur rouge.
    only_player_detection : bool
        Indique si on ne doit détecter que le joueur (True) ou tous les objets rouges (False).

    Retourne :
    tuple (np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, tuple (int, int))
        - Image finale avec le joueur ou les objets détectés.
        - Image seuillée en niveaux de gris.
        - Image seuillée avec les figures dessinées.
        - Image filtrée pour la couleur rouge.
        - Image filtrée avec les figures dessinées.
        - Position du joueur ou de l'objet détecté.
    """
    color = red_filter(frame,low_color,high_color)  # Filtrage de la couleur rouge
    threshold = threshold_filter(color)  # Application du seuillage

    # On ajoute un canal de couleur aux images de seuillage
    threshold_bgr = cv2.cvtColor(threshold,cv2.COLOR_GRAY2BGR)

    if only_player_detection:
        # Détection du joueur uniquement
        frame_figure, position = draw_figure_player(threshold,frame)
        threshold_figure = draw_figure_player(threshold,threshold_bgr)[0]
        color_figure = draw_figure_player(threshold,color)[0]
    else:
        # Détection de tous les objets rouges
        frame_figure, position = draw_figure_color(threshold,frame)
        threshold_figure = draw_figure_color(threshold,threshold_bgr)[0]
        color_figure = draw_figure_color(threshold,color)[0]

    return frame_figure, threshold, threshold_figure, color, color_figure, position