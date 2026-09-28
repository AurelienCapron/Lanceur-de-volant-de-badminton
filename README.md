# Lanceur de volant de badminton automatisé

Projet de TIPE : modélisation d'une assistance mécanique pour l'entraînement au badminton, combinant détection du joueur par vision par ordinateur et pilotage d'un lanceur motorisé.

*English summary: Automated badminton shuttlecock launcher developed as an engineering project (TIPE). It uses stereo computer vision (Python / OpenCV) to track a player's 2D position on the court via triangulation (depth and azimuth) and controls an Arduino-based motorized launcher over serial communication.*

---

## Principe de fonctionnement

L'objectif du projet est de localiser un joueur en temps réel sur un demi-terrain de badminton afin d'orienter automatiquement un lanceur de volants selon différents modes d'entraînement.

Le système repose sur quatre briques :
1. **Détection du joueur (OpenCV)** : Après un premier prototypage avec YOLO, la détection temps réel est assurée par un filtrage colorimétrique dans l'espace HSV suivi d'un seuillage binaire et d'une extraction du contour principal.
2. **Localisation par stéréovision** : Deux caméras alignées sur un même plan vertical et séparées d'une distance fixe mesurent les angles d'observation du joueur. La position (profondeur et azimut) est déduite par triangulation.
3. **Logique d'entraînement et visualisation 2D** : Affichage en temps réel de la position du joueur sur un terrain virtuel. Deux modes de visée sont implémentés : tir vers une position fixe ou tir aléatoire dans un rayon de difficulté autour du joueur pour forcer le déplacement.
4. **Commande matérielle (Arduino UNO)** : Envoi des consignes (azimut, altitude, puissance, fréquences, niveau de difficulté) par liaison série USB pour piloter les servomoteurs d'orientation et gérer le boîtier de contrôle (bouton de sélection de niveau et LEDs d'état).

Une étude balistique prenant en compte les frottements aérodynamiques du volant ($C_x \cdot S$) complète le modèle pour relier la distance de tir aux paramètres de lancement.

---

## Architecture des fichiers

* `Programme_principale.py` : Boucle principale d'acquisition des deux caméras, calculs géométriques, affichage de l'interface (flux vidéo + terrain 2D) et communication série.
* `Detection_joueur.py` : Fonctions de traitement d'image (conversion BGR vers HSV, masque de couleur, seuillage et détection du rectangle englobant).
* `Variables_positions.py` : Calculs optiques et géométriques (distance focale, champ de vision, triangulation de la profondeur et de l'azimut, coordonnées du cercle de difficulté).
* `Terrain_badminton.py` : Modélisation graphique du terrain de badminton aux cotes officielles et affichage des cônes de vision.
* `Determination_filtre.py` : Script de calibration permettant de récupérer les valeurs HSV d'un pixel au clic et d'ajuster les seuils via des barres de réglage.
* `Calibrage_camera.py` : Outil d'aide à l'alignement physique des deux caméras.
* `Transfert_donnees_lanceur.py` : Détection des ports USB disponibles et ouverture de la connexion série avec le microcontrôleur.
* `Interface_utilisateur.py` : Lecture des commandes saisies dans le terminal pour modifier les paramètres à la volée.
* `Texte_image.py` : Incrustation des données (distance, largeur, angles, azimut) sur le retour vidéo.
* `Code_arduino.ino` : Programme embarqué sur l'Arduino UNO assurant le décodage des trames série et l'asservissement des servomoteurs.

---

## Prérequis

### Logiciel
Python 3 avec les bibliothèques suivantes :

```bash
pip install numpy==2.2.3 opencv-python==4.11.0.86 pyserial==3.5
