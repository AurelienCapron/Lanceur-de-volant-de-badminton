"""
Nom du fichier : Interface_utilisateur.py
Auteur : CAPRON Aurélien
Date : 16/02/2025
Description :
    Ce script informe des différents niveaux de difficulté pour un système de lancement de volant. 
    Il informe également les symboles à utiliser pour modifier certains paramètres, tout en intégrant une gestion interactive de ceux-ci.
"""

import threading

class ModifiedParameter:
    """
    Classe permettant de modifier dynamiquement les paramètres du rayon et de la fréquence en fonction de la difficulté
    """
    def __init__(self, valeur_initiale="Valeur initiale"):
        self.ma_variable = valeur_initiale  # Stocke la valeur initiale de la variable
        self.running = True  # Indicateur pour gérer l'arrêt propre du programme
        self.valeur_modifiee = valeur_initiale  # La variable qui sera mise à jour dynamiquement

        # Lancement d'un thread en mode daemon pour surveiller les entrées utilisateur
        self.thread_input = threading.Thread(target=self.surveiller_input, daemon=True)
        self.thread_input.start()

    def surveiller_input(self):
        """Écoute en continu les entrées utilisateur pour mettre à jour la variable"""
        while self.running:
            user_input = input()
            if user_input.strip():  # Vérifie que l'entrée utilisateur n'est pas vide
                self.valeur_modifiee = user_input  # Mise à jour de la variable modifiée

def input_analysis(written_value):
    """
    Analyse l'entrée utilisateur et détermine si elle est une modification de fréquence ou de rayon
    
    Retourne :
    - (1, valeur) si la valeur est précédée de "!" (indique une fréquence).
    - (2, valeur) si la valeur est un entier sans "!" (indique un rayon). 
    - (3, valeur) si la valeur ne peut pas être convertie en entier.
    """
    frequency_throw = False
    frequency_launcher = False
    radius = False
    permanent_depth = False
    permanent_width = False
    if isinstance(written_value, str):
        if written_value in ["True","true","False","false"]:
            return (1, written_value)
        elif written_value in ["1","2","3"]:
            return (2,written_value)
        elif written_value[0] in ["V","v"]:
            frequency_throw = True
        elif written_value[0] in ["F","f"]:
            frequency_launcher = True
        elif written_value[0] in ["R","r"]:
            radius = True
        elif written_value[0] in ["P","p"]:
            permanent_depth = True
        elif written_value[0] in ["L","l"]:
            permanent_width = True
        written_value = written_value[1:]
    try:
        written_value = int(written_value)
        abs_written_value = abs(written_value)
        if frequency_throw:
            return (3, abs_written_value)
        elif frequency_launcher:
            return (4, abs_written_value)
        elif radius:
            return (5, abs_written_value)
        elif permanent_depth:
            return (6, abs_written_value)
        elif permanent_width:
            return (7, written_value)
        else:
            return (8, written_value)
    except:
        return (8, written_value)

# Messages correspondant aux niveaux de difficulté
level_1 = "Le volant est lancé sur le joueur"
level_2 = "Le volant est lancé de façon aléatoire dans un cercle de rayon choisi"
level_3 = "Le volant est lancé de façon aléatoire sur le rayon du cercle choisi"

def difficulty_choice():
    """
    Indique les différents niveaux de difficulté et les symboles à utiliser pour modifier certains paramètres.
    """
    print("Niveaux de la difficulté :")
    print(f"- \033[32mNiveau 1\033[0m : {level_1}")
    print(f"- \033[33mNiveau 2\033[0m : {level_2}")
    print(f"- \033[31mNiveau 3\033[0m : {level_3}\n")

    print("Veuillez indiquer \033[32mTrue\033[0m ou \033[31mFalse\033[0m pour gérer l'activation du mode de suivi.\n")
    print("Veuillez indiquer \033[34m1\033[0m, \033[34m2\033[0m ou \033[34m3\033[0m pour changer l'affichage des caméras.")
    print("- \033[34m1\033[0m : Affichage sans modification")
    print("- \033[34m2\033[0m : Affichage du seuillage de la couleur filtrée")
    print("- \033[34m3\033[0m : Affichage seulement de la couleur filtrée\n")

    print("Pour modifier un paramètre dynamiquement, utilisez les préfixes suivants :")
    print("- 'V' : Ajuster la fréquence d'envoi du volant")
    print("- 'F' : Ajuster la fréquence de mis à jour du lanceur")
    print("- 'R' : Modifier le rayon de difficulté")
    print("- 'P' : Changer la profondeur de la position permanente du tir du volant")
    print("- 'L' : Changer la largeur de la position permanente du tir du volant\n")
