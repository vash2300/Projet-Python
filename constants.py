WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05
CAR_DECELERATION = 0.05
CAR_TURN_SPEED = 1
CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    CIRCUIT_SELECT = "circuit_select" #selection du circuit sur le menu
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)

# --- Paramètres généraux de la physique du drift ---
SPEED_MIN = 1.5 #Vitesse minimale pour activer le drift (c'est un seuil)
STEERING_MIN = 0.5 #Seuil minimum de braquage pour activer le drift
MAX_SPEED = 5.0 #Vitesse maximal de la voiture en D
MAX_REVERSE = -2.5 #Vitesse max en mode R
AIR_FRICTION = 0.005 #Frottements due à l'air (NRML_FRICTION)
DRIFT_FRICTION = 0.025 #Frottements due au drift
K_NRML = 0.15 #Vitesse de réalignement normale (qd la voiture adhère)
K_DRIFT = 0.025 #Vitesse de réalignement en drift

# --- Paramètre de terrains ---

