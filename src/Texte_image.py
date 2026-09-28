"""
Nom du fichier : Texte_image.py
Auteur : CAPRON Aurélien
Date : 14/02/2025
Description :
    Ce script permet d'ajouter différents textes sur une image, notamment des informations relatives à la position,
    la profondeur, la largeur, les angles, et d'autres données associées. Les textes sont affichés selon des paramètres 
    définis et sont personnalisables (police, taille, couleur, etc.).
"""

import cv2
import numpy as np

def text_position(img,position,fontFace,fontScale,color,thickness,height):
    """
    Affiche la position du joueur sur l'image.
    """
    cv2.putText(img,f"Position = {position}",(15,height),fontFace,fontScale,color,thickness)

def text_depth(img,depth_player,fontFace,fontScale,color,thickness,height):
    """
    Affiche la profondeur du joueur sur l'image.
    """
    cv2.putText(img,f"Profondeur = {round(depth_player)} mm",(15,height),fontFace,fontScale,color,thickness)
    
def text_width(img,width_player,fontFace,fontScale,color,thickness,height):
    """
    Affiche la largeur du joueur sur l'image.
    """
    cv2.putText(img,f"Largeur = {round(width_player)} mm",(15,height),fontFace,fontScale,color,thickness)

def text_angle(img,angle,fontFace,fontScale,color,thickness,height):
    """
    Affiche l'angle de la caméra sur l'image.
    """
    cv2.putText(img,f"Angle camera = {round(np.degrees(angle))} deg",(15,height),fontFace,fontScale,color,thickness)

def text_total_angle(img,angle,fontFace,fontScale,color,thickness,height):
    """
    Affiche l'angle total sur l'image.
    """
    cv2.putText(img,f"Angle total = {round(np.degrees(angle))} deg",(15,height),fontFace,fontScale,color,thickness)

def text_azimuth(img,angle,fontFace,fontScale,color,thickness,height):
    """
    Affiche l'azimut du joueur sur l'image.
    """
    cv2.putText(img,f"Azimut = {round(np.degrees(angle))} deg",(15,height),fontFace,fontScale,color,thickness)

def text_layout(img,depth_player,width_player,position,angle,total_angle,azimut,fontFace,fontScale,color,thickness,display):
    """
    Affiche plusieurs informations sur l'image en fonction des options définies dans `display`.
    """
    # Initialisation de la hauteur du texte
    height_text = 0

    # Si display est une liste contenant uniquement [True], on l'étend pour afficher tous les éléments
    if display == [True] : 
        display *= 6

    if display[0]:  # Afficher la position
        height_text += 30
        text_position(img,position,fontFace,fontScale,color,thickness,height_text)
    if display[1]:  # Afficher la profondeur
        height_text += 30
        text_depth(img,depth_player,fontFace,fontScale,color,thickness,height_text)
    if display[2]:  # Afficher la largeur
        height_text += 30
        text_width(img,width_player,fontFace,fontScale,color,thickness,height_text)
    if display[3]:  # Afficher l'angle de la caméra
        height_text += 30
        text_angle(img,angle,fontFace,fontScale,color,thickness,height_text)
    if display[4]:  # Afficher l'angle total
        height_text += 30
        text_total_angle(img,total_angle,fontFace,fontScale,color,thickness,height_text)
    if display[5]:  # Afficher l'azimut
        height_text += 30
        text_azimuth(img,azimut,fontFace,fontScale,color,thickness,height_text)

def image_display(img,depth_player,width_player,position_right,angle,total_angle,azimut,fontFace,fontScale,text_color,thickness,text_display,text_window):
    """
    Affiche les informations sur l'image en fonction des options de texte spécifiées.
    """
    if set(text_display) != {False}:  # Si au moins une information est à afficher
        text_layout(img,depth_player,width_player,position_right,angle,total_angle,azimut,fontFace,fontScale,text_color,thickness,text_display)
    return img