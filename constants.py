import os

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05
CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)


# ======================================================================
# AJOUTS PARTIE "TERRAINS ET CIRCUITS"
# ======================================================================

# Dossier contenant les fichiers texte des circuits (à côté de ce fichier)
CIRCUITS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "circuits")

# --- Boost (valeurs par défaut d'un BoostBlock) ---
# La force est un bonus d'accélération, la durée est en nombre de frames.
# Ces valeurs sont à régler avec la partie "Voiture et contrôles".
BOOST_STRENGTH = 0.15
BOOST_DURATION = 60

# --- Propriétés physiques des terrains ---
# Format : (traction, drift_threshold, drift_friction)
#   traction         : facilité à accélérer / freiner (1.0 = maximale)
#   drift_threshold  : angle (en radians) entre l'orientation de la voiture
#                      et sa vitesse au-delà duquel elle dérape.
#                      Plus il est grand, plus il est difficile de déraper.
#   drift_friction   : proportion de vitesse perdue par frame pendant un
#                      dérapage (0 = aucun frottement, 1 = arrêt immédiat)
# Ce sont des valeurs de départ, à ajuster en jouant.
TERRAIN_STATS = {
    "road":  (1.0, 0.80, 0.080),
    "grass": (0.6, 0.50, 0.050),
    "dirt":  (0.5, 0.30, 0.030),
    "ice":   (0.2, 0.10, 0.002),
    "void":  (0.0, 0.00, 0.000),
}

# --- Couleurs des terrains ---
TERRAIN_COLORS = {
    "road":  (85, 85, 95),
    "grass": (60, 140, 60),
    "dirt":  (150, 105, 60),
    "ice":   (170, 220, 240),
    "void":  (10, 10, 18),
}

# --- Couleurs des symboles de blocs (clé = label du bloc) ---
BLOCK_COLORS = {
    "1": (255, 90, 90),     # départ joueur 1
    "2": (90, 150, 255),    # départ joueur 2
    "C": (255, 200, 0),     # point de passage
    "L": (240, 240, 240),   # ligne d'arrivée
    "B": (0, 220, 130),     # boost
}
