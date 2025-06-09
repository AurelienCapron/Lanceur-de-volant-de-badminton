import numpy as np
from Variables_positions import dimension_scale,random_point_circle,position_on_court,position_court_base,angle_position_launcher

dimension_real = (13400,6100,3)
position_net = (dimension_real[0],6100,3)

position_launcher = (3500,0)  # Position du lanceur par rapport à la base du terrain (en mm) : (abscisse, ordonnée) 
position_cameras = (3500,0)   # Position de l'installation caméra par rapport à la base du terrain (en mm) : (abscisse, ordonnée)

height_net = 1500 # Hauteur du filet (en mm)

def circle_difficulty_on_court(depth_player,width_player,position_launcher,radius_difficulty):
    depth = False
    width = 0

    depth_launcher_court = dimension_real[0]-position_launcher[1]
    width_left_launcher_court = position_launcher[0]
    width_right_launcher_court = dimension_real[1]-position_launcher[0]

    if depth_player - radius_difficulty > depth_launcher_court:
        depth = True
    if width_player >= 0 and width_player-radius_difficulty > width_right_launcher_court:
        width = 1
    elif width_player < 0 and abs(width_player)-radius_difficulty > width_left_launcher_court:
        width = -1

    if width == -1 and depth:
        return (-width_left_launcher_court,depth_launcher_court)
    elif width == 1 and depth:
        return (width_right_launcher_court,depth_launcher_court)
    elif width == -1:
        return (-width_left_launcher_court,depth_player)
    elif width == 1:
        return (width_right_launcher_court,depth_player)
    elif depth == True:
        return (width_player,depth_launcher_court)
    return True

def position_difficulty_on_court(frame, depth, width, position_launcher, level, radius, real_condition_launcher):
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

    circle_difficulty = circle_difficulty_on_court(depth,width,position_launcher,radius)
    
    # Si le niveau de difficulté est 1, on garde la position initiale
    if level == 1:
        return width, depth
    else :
        if circle_difficulty == True:
            # Génération d'une position aléatoire dans un rayon autour de la position initiale
            x, y = random_point_circle(depth, width, level, radius)

            # Vérification que la position générée est bien dans les limites du terrain
            while (x not in range(0,width_frame)) or (y not in range(0,depth_max)):
                x, y = random_point_circle(depth, width, level, radius)

            return x, y
        else:
            return circle_difficulty

def difficulty_variable(frame,depth_player,width_player,level_difficulty,radius_difficulty,real_condition_launcher):
    """
    Calcule les variables de difficulté en fonction de la position du joueur et des paramètres de difficulté du jeu.
    """
    position_player_court = position_on_court(frame,depth_player,width_player)

    position_player_court_base = position_court_base(frame,position_player_court)
    position_difficulty_court = position_difficulty_on_court(frame,position_player_court[1],position_player_court[0],level_difficulty,radius_difficulty,real_condition_launcher)
    position_difficulty_base = position_court_base(frame,position_difficulty_court)

    azimut_difficulty = angle_position_launcher(position_difficulty_base[0],position_difficulty_base[1])

    return position_player_court, position_player_court_base, position_difficulty_court, position_difficulty_base, azimut_difficulty

def distance_player(depth,width):
    return np.sqrt(depth**2+abs(width)**2)

def distance_net(position_launcher,position_net):
    return position_net[0]-position_launcher[0]

def valid_throw(distance_player,height_net,height_launcher):
    """
    height_throw = equation differentielle en fontion de la distance du joueur (distance_player) et la hauteur du lanceur (height_launcher)
    if height_throw > height_net:
        return True
    return False
    """
    pass

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1️⃣ Création d'un graphique Matplotlib
fig, ax = plt.subplots(figsize=(4, 3))  # Taille de l'image
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y, label="sin(x)", color="b")
ax.legend()
ax.set_title("Courbe de sin(x)")

# 2️⃣ Convertir la figure Matplotlib en image OpenCV
fig.canvas.draw()  # Dessiner la figure
img_matplotlib = np.array(fig.canvas.renderer.buffer_rgba())  # Convertir en array
img_matplotlib = cv2.cvtColor(img_matplotlib, cv2.COLOR_RGBA2BGR)  # Convertir en BGR (format OpenCV)

plt.close(fig)  # Fermer la figure pour économiser de la mémoire

# 3️⃣ Charger une image OpenCV pour concaténer
img_opencv = np.zeros((300, 400, 3), dtype=np.uint8)  # Image noire de même taille

# 4️⃣ Concaténer verticalement avec cv2.vconcat
concat_image = cv2.vconcat([img_opencv, img_matplotlib])

# 5️⃣ Afficher le résultat
cv2.imshow("Concatenated Image", concat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""