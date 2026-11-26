import os

# ======================================================================
# PARAMÈTRES GÉNÉRAUX
# ======================================================================

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# ======================================================================
# PARAMÈTRES VOITURE
# ======================================================================

CAR_ACCELERATION = 0.05
CAR_DECELERATION = 0.05
CAR_TURN_SPEED = 1

CAR_WIDTH = 30
CAR_HEIGHT = 50

# ======================================================================
# ÉTATS DU JEU
# ======================================================================

class GameState:
    MENU = "menu"
    CIRCUIT_SELECT = "circuit_select"
    RACING = "racing"


# ======================================================================
# COULEURS UI
# ======================================================================

COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)


# ======================================================================
# PARAMÈTRES GÉNÉRAUX DE LA PHYSIQUE DU DRIFT
# ======================================================================

SPEED_MIN = 1.5
STEERING_MIN = 0.5

MAX_SPEED = 5.0
MAX_REVERSE = -2.5

AIR_FRICTION = 0.005
DRIFT_FRICTION = 0.025

K_NRML = 0.15
K_DRIFT = 0.025


# ======================================================================
# CIRCUITS
# ======================================================================

# Dossier contenant les fichiers texte des circuits
# (à côté de ce fichier)
CIRCUITS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "circuits"
)


# ======================================================================
# BOOST
# ======================================================================

# Force du boost : bonus d'accélération
BOOST_STRENGTH = 0.15

# Durée du boost en frames (60 FPS = 1 seconde)
BOOST_DURATION = 60


# ======================================================================
# PROPRIÉTÉS PHYSIQUES DES TERRAINS
# Format : (traction, drift_threshold, drift_friction)
# ======================================================================

TERRAIN_STATS = {
    "road":  (1.0, 0.80, 0.080),
    "grass": (0.6, 0.50, 0.050),
    "dirt":  (0.5, 0.30, 0.030),
    "ice":   (0.2, 0.10, 0.002),
    "void":  (0.0, 0.00, 0.000),
}


# ======================================================================
# COULEURS DES TERRAINS
# ======================================================================

TERRAIN_COLORS = {
    "road":  (85, 85, 95),
    "grass": (60, 140, 60),
    "dirt":  (150, 105, 60),
    "ice":   (170, 220, 240),
    "void":  (10, 10, 18),
}


# ======================================================================
# COULEURS DES BLOCS
# ======================================================================

# Clé = label du bloc

BLOCK_COLORS = {
    "1": (255, 90, 90),      # Départ joueur 1
    "2": (90, 150, 255),     # Départ joueur 2
    "C": (255, 200, 0),       # Point de passage (checkpoint)
    "L": (240, 240, 240),     # Ligne d'arrivée
    "B": (0, 220, 130),       # Boost
}