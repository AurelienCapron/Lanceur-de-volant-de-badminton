"""
Nom du fichier : Transfert_donnees_lanceur.py
Auteur : CAPRON Aurélien
Date : 15/02/2025
Description :
    Ce script permet d'établir une connexion série via un port USB pour communiquer avec un dispositif externe, comme un lanceur.
    Il vérifie la disponibilité du port USB et tente une connexion avec des paramètres de communication spécifiés.
"""

import serial
import serial.tools.list_ports

def connection_port(port_usb):
    """
    Vérifie si le port USB spécifié est disponible parmi les ports série présents sur la machine.
    """
    # Vérification des ports disponibles
    ports_disponibles = [port.device for port in serial.tools.list_ports.comports()]
    if port_usb not in ports_disponibles:
        print(f"\nPort \033[34m{port_usb}\033[0m non trouvé\n")
        print("Ports disponibles :")
        for port in ports_disponibles:  # Affichage des ports diponibles
            print(f"- {port}")
        print()
        return False  # Le port spécifié n'est pas disponible
    return True  # Le port spécifié est disponible

def connexion_successful(port_usb,baudrate):
    """
    Tente de se connecter au port USB spécifié avec le débit en bauds donné. Si la connexion échoue, un message d'erreur est affiché.
    """
    try:
        # Tente d'ouvrir le port série avec les paramètres spécifiés
        ser = serial.Serial(port_usb, baudrate, timeout=1)
        print(f"\nConnexion établie sur \033[34m{port_usb}\033[0m\n")
    except serial.SerialException as error:
        # Si la connexion échoue, un message d'erreur est affiché
        print(f"\nImpossible de se connecter au port USB : \n\033[31m{error}\033[0m\n")
        exit(1)  # Arrêt du programme en cas d'échec de la connexion
    return ser  # Retourne l'objet Serial pour la communication série