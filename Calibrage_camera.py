"""
Nom du fichier : Calibrage_camera.py
Auteur : CAPRON Aurélien
Date : 11/02/2025
Description :
    Ce script permet d'afficher deux flux vidéo en direct provenant de deux caméras, en ajoutant un curseur central (ligne et cercle)
    sur chaque flux pour faciliter le calibrage des caméras. Il affiche ces vidéos côte à côte et attend l'appui sur la touche 'q'
    pour quitter.
"""

import cv2

def curseur(frame, r, thickness):
    """
    Ajoute un curseur visuel (une croix et un cercle) au centre d'un flux vidéo.
    """
    # Obtention des dimensions de l'image (hauteur, largeur, canaux de couleur)
    x, y, _ = frame.shape

    # Calcul des coordonnées du centre de l'image
    cx = int(x/2)
    cy = int(y/2)

    # Dessin de la croix centrale : deux lignes perpendiculaires
    cv2.line(frame,(0,cx),(y,cx),(0,0,255),thickness)  # Ligne horizontale
    cv2.line(frame,(cy,0),(cy,x),(0,0,255),thickness)  # Ligne verticale

    cv2.circle(frame,(cy,cx),r,(0,0,255),thickness)  # Cercle rouge au centre

# Ouverture des caméras
cap_left = cv2.VideoCapture(1)
cap_right = cv2.VideoCapture(0)

# Paramètres du curseur
radius = 75    # Rayon du cercle à dessiner
thickness = 4  # Épaisseur des lignes du curseur

while True:
    # Lecture des frames des deux caméras
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    # Vérification que les deux caméras fonctionnent correctement
    if not ret_left or not ret_right:
        print("\n\033[31mProblème lors de la connexion aux caméras\033[0m\n")
        break

    # Ajout du curseur sur les frames des caméras
    curseur(frame_left, radius, thickness)
    curseur(frame_right, radius, thickness)

    # Fusion des deux flux vidéo en une seule image (côte à côte)
    combined = cv2.hconcat([frame_left,frame_right])

    # Affichage de l'image combinée
    cv2.imshow("Cameras avec curseur",combined)

    # Vérifie si l'utilisateur appuie sur la touche 'Échap' pour quitter la boucle principale
    if cv2.waitKey(1) == 27:
        break

# Libération des ressources de capture vidéo et fermeture des fenêtres
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()