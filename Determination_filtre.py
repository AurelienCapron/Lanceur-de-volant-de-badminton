"""
Nom du fichier : Determination_filtre.py
Auteur : CAPRON Aurélien
Date : 12/02/2025
Description :
    Ce script est conçu pour déterminer les seuils HSV (teinte, saturation, valeur) qui permettent de détecter un objet (probablement un joueur) 
    en utilisant une méthode interactive avec des trackbars et une autre méthode basée sur des tests pour trouver des plages HSV optimales.
    Il permet également de sélectionner un filtre de couleur en cliquant sur l'objet ou la personne à filter.
    Il utilise OpenCV pour capturer des images, ajuster les seuils HSV en temps réel et vérifier la précision de la détection.
"""

import cv2
import numpy as np
from Detection_joueur import final_frame

# Fonction vide utilisée pour les trackbars
def nothing(x): 
    pass

def code_hsv_color():
    """
    Affiche une fenêtre interactive permettant d'ajuster dynamiquement une couleur en espace HSV.

    Cette fonction crée une fenêtre OpenCV avec trois trackbars pour ajuster les valeurs :
    - H (Teinte) : [0, 179] (car OpenCV limite la teinte à cette plage)
    - S (Saturation) : [0, 255]
    - V (Valeur/Luminosité) : [0, 255]

    La couleur sélectionnée est affichée en temps réel dans la fenêtre en convertissant 
    l'image HSV en BGR pour OpenCV.

    L'utilisateur peut quitter l'application en appuyant sur la touche 'Échap'.
    """
    # Crée une fenêtre nommée "Code HSV de la couleur"
    cv2.namedWindow("Code HSV de la couleur")

    # Ajoute trois trackbars pour modifier les valeurs H, S et V en temps réel
    # - H (Teinte) varie de 0 à 179
    # - S (Saturation) varie de 0 à 255
    # - V (Valeur/Luminosité) varie de 0 à 255
    cv2.createTrackbar("H", "Code HSV de la couleur", 0, 179, nothing)
    cv2.createTrackbar("S", "Code HSV de la couleur", 255, 255, nothing)
    cv2.createTrackbar("V", "Code HSV de la couleur", 255, 255, nothing)

    # Crée une image vide (noire) en HSV avec une taille de 250x500 pixels
    img_hsv = np.zeros((250, 500, 3), np.uint8)

    while True:
        # Récupère les positions actuelles des trackbars pour H, S et V
        h = cv2.getTrackbarPos("H", "Code HSV de la couleur")
        s = cv2.getTrackbarPos("S", "Code HSV de la couleur")
        v = cv2.getTrackbarPos("V", "Code HSV de la couleur")

        # Remplit toute l'image avec la couleur HSV sélectionnée
        img_hsv[:] = (h, s, v)

        # Convertit l'image HSV en BGR pour l'affichage avec OpenCV
        img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        cv2.imshow("Code HSV de la couleur", img_bgr)

        # Vérifie si l'utilisateur appuie sur la touche 'Échap' pour quitter la boucle principale
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

def manual_filter_determination():
    """
    Crée une fenêtre avec des trackbars (curseurs) pour ajuster les valeurs HSV.
    L'utilisateur peut manipuler les curseurs pour ajuster les plages de couleur et observer les effets en temps réel.
    """
    # Créer une fenêtre pour les trackbars
    cv2.namedWindow("Filtre de couleur en temps reel")

    # Créer des trackbars pour ajuster les plages HSV min et max
    cv2.createTrackbar("H Min", "Filtre de couleur en temps reel", 0, 179, nothing)    # Plage de teinte minimale
    cv2.createTrackbar("S Min", "Filtre de couleur en temps reel", 0, 255, nothing)    # Plage de saturation minimale
    cv2.createTrackbar("V Min", "Filtre de couleur en temps reel", 0, 255, nothing)    # Plage de valeur minimale
    cv2.createTrackbar("H Max", "Filtre de couleur en temps reel", 179, 179, nothing)  # Plage de teinte maximale
    cv2.createTrackbar("S Max", "Filtre de couleur en temps reel", 255, 255, nothing)  # Plage de saturation maximale
    cv2.createTrackbar("V Max", "Filtre de couleur en temps reel", 255, 255, nothing)  # Plage de valeur maximale

    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)

    while True:
        # Lire une image de la caméra
        _, frame = cap.read()
        
        # Récupérer les valeurs des trackbars (plages HSV ajustées par l'utilisateur)
        h_min = cv2.getTrackbarPos("H Min", "Filtre de couleur en temps reel")
        s_min = cv2.getTrackbarPos("S Min", "Filtre de couleur en temps reel")
        v_min = cv2.getTrackbarPos("V Min", "Filtre de couleur en temps reel")
        h_max = cv2.getTrackbarPos("H Max", "Filtre de couleur en temps reel")
        s_max = cv2.getTrackbarPos("S Max", "Filtre de couleur en temps reel")
        v_max = cv2.getTrackbarPos("V Max", "Filtre de couleur en temps reel")

        # Définir les seuils HSV pour la détection
        lower_bound = np.array([h_min, s_min, v_min])  # Limite inférieure HSV
        upper_bound = np.array([h_max, s_max, v_max])  # Limite supérieure HSV

        # Appliquer le filtre de détection avec les valeurs HSV définies
        color = final_frame(frame,lower_bound,upper_bound,True)[3]

        # Afficher le résultat de la détection
        cv2.imshow("Filtre de couleur en temps reel", color)

        # Vérifie si l'utilisateur appuie sur la touche 'Échap' pour quitter la boucle principale
        if cv2.waitKey(1) == 27:
            break

    # Libération des ressources de la caméra
    cap.release()
    cv2.destroyAllWindows()

def automatic_filter_determination():
    """
    Effectue une série de tests pour déterminer les plages de valeurs HSV qui permettent de détecter l'objet avec précision.
    Cette fonction parcourt différentes plages de teinte, saturation et valeur, puis teste la détection dans ces plages.
    Elle collecte et renvoie les valeurs HSV qui donnent des résultats précis.
    """
    # Valeurs de test initiales pour les plages HSV minimales et maximales
    (h_test_min,s_test_min,v_test_min) = (161,145,75)
    (h_test_max,s_test_max,v_test_max) = (172,160,90)
    (h_max,s_max,v_max) = (179,255,255)

    posible_hsv = []  # Liste pour stocker les plages HSV possibles
    tolerance = 1  # Tolérance pour vérifier la précision de la détection
    number_image_verification = 50  # Nombre d'images à vérifier pour chaque plage HSV

    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(1)

    # Parcours des plages de test pour chaque composant HSV (teinte, saturation, valeur)
    for h in range(h_test_min,h_test_max):
        for s in range(s_test_min,s_test_max):
            for v in range(v_test_min,v_test_max):
                flag = True  # Variable pour suivre la précision de la détection

                # Lire une image de la caméra
                _, frame = cap.read()

                # Récupérer la position de référence avec les plages HSV actuelles
                x_ref, y_ref = final_frame(frame,(h,s,v),(h_max,s_max,v_max),True)[5]
                print("HSV :", h,s,v)
                print("Position de reference :", (x_ref,y_ref))

                # Vérification de la précision de la détection pour plusieurs images
                for i in range(number_image_verification):
                    _, frame = cap.read()
                    position = final_frame(frame,(h,s,v),(h_max,s_max,v_max),True)[5]
                    print(position)
                    # Si la position et détectée et/ou est trop éloignée de la référence, abandonner cette plage HSV
                    if (position[0] not in range(x_ref-tolerance,x_ref+tolerance+1)) or (position[1] not in range(y_ref-tolerance,y_ref+tolerance+1)) or (x_ref,y_ref)==(0,0):
                        flag = False

                print(f"HSV possible : {posible_hsv}\n")

                # Si cette plage HSV donne une détection précise, l'ajouter à la liste des plages possibles
                if flag: posible_hsv.append((h,s,v))
                
    # Libération des ressources de la caméra
    cap.release()
    cv2.destroyAllWindows()

    return posible_hsv  # Retourner les plages HSV possibles

#--------- Fonctions pour obtenir un filtre de couleur du pixel cliqué ---------

# Valeur HSV initiale, utilisée comme point de départ pour le filtrage des couleurs
hsv_pixel = np.array([170, 215, 105])  

def get_hsv_color(event, x, y, flags, param):
    """
    Fonction de rappel (callback) pour récupérer la couleur HSV d'un pixel cliqué.

    Lorsqu'un clic gauche est détecté sur l'image affichée, cette fonction :
    - Récupère la couleur du pixel correspondant en format BGR.
    - Convertit cette couleur en format HSV.
    - Stocke la valeur HSV dans une variable globale.
    """
    global hsv_pixel  # Utilisation d'une variable globale pour stocker la valeur HSV du pixel cliqué

    if event == cv2.EVENT_LBUTTONDOWN:  # Vérifie si un clic gauche est effectué
        frame = param[0]  # Récupère la dernière image capturée
        pixel = frame[y, x]  # Récupère la couleur BGR du pixel cliqué aux coordonnées (x, y)

        # Convertit la couleur du format BGR en HSV et stocke le résultat dans hsv_pixel
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]  

def filter_determination(capture, camera_name):
    """
    Fonction permettant de déterminer un filtre HSV basé sur un clic de souris.

    Cette fonction :
    - Permet de cliquer sur un pixel pour récupérer sa couleur HSV.
    - Applique un filtre autour de cette couleur avec une plage définie ('range_value').
    - Affiche l'image originale et l'image filtrée en temps réel.
    - Quitte lorsque la touche 'Échap' (ESC) est pressée.
    """
    global hsv_pixel  # Variable globale contenant la valeur HSV sélectionnée

    cv2.namedWindow(camera_name)  # Crée une fenêtre d'affichage OpenCV

    cv2.createTrackbar("Largeur filtre :", camera_name, 0, 100, nothing) # Créer une trackbar pour ajuster la plage HSV
    cv2.setTrackbarPos("Largeur filtre :", camera_name, 50)  # Modifier la position initiale à 50

    while True:
        ret, frame = capture.read()  # Capture une nouvelle image depuis la caméra
        if not ret:
            print(f"\033[31mErreur: Impossible de lire la frame de la caméra :\033[0m {camera_name}\n")
            break

        # Associer la fonction de récupération de couleur HSV au clic de souris
        cv2.setMouseCallback(camera_name, get_hsv_color, [frame])

        # Récupérer la valeur du trackbar (plage HSV ajustées par l'utilisateur)
        range_value = cv2.getTrackbarPos("Largeur filtre :", camera_name)

        # Récupération des composants H, S et V de la couleur sélectionnée et conversion en entier
        h, s, v = int(hsv_pixel[0]), int(hsv_pixel[1]), int(hsv_pixel[2])

        # Détermination des bornes inférieures, en s'assurant qu'elles restent dans les limites (min 0)
        h_min = max(h - range_value, 0)
        s_min = max(s - range_value, 0)
        v_min = max(v - range_value, 0)

        # Détermination des bornes supérieures, en respectant les valeurs maximales HSV (H: 179, S/V: 255)
        h_max = min(h + range_value, 179)  # La teinte (H) varie de 0 à 179 en OpenCV
        s_max = min(s + range_value, 255)  # La saturation (S) varie de 0 à 255
        v_max = min(v + range_value, 255)  # La valeur (V) varie de 0 à 255

        # Définition des plages de couleurs HSV pour le filtrage
        low_color = np.array([h_min, s_min, v_min], dtype=int)
        high_color = np.array([h_max, s_max, v_max], dtype=int)

        # Conversion de l'image originale en format HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Création du masque en fonction des bornes HSV définies
        mask = cv2.inRange(hsv_frame, low_color, high_color)

        # Application du masque à l'image originale pour afficher uniquement les pixels filtrés
        result_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Fusionner l'image originale et l'image filtrée verticalement pour affichage
        combined = cv2.hconcat([frame, result_frame])

        # Afficher l'image mise à jour dans la fenêtre OpenCV
        cv2.imshow(camera_name, combined)

        # Quitter la boucle si l'utilisateur appuie sur la touche 'Échap' (code ASCII 27)
        if cv2.waitKey(1) == 27:  
            break

    # Fermer toutes les fenêtres OpenCV avant de quitter
    cv2.destroyAllWindows()

    # Retourner les bornes HSV utilisées pour le filtrage
    return low_color, high_color


#--------- Appels aux fonctions pour déterminer les seuils (commentées pour ne pas les exécuter automatiquement) ---------

#code_hsv_color()
#manual_filter_determination()
#automatic_filter_determination()