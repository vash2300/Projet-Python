import pygame
import math
from constants import (CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, CAR_TURN_SPEED, MAX_SPEED)



class Car:
    """
    Voiture de course.
    La classe definie les positions x et y de la voiture.
    Elle définie sa vitesse et son angle de braquage en degrés.
    Elle à un sprite : rectangle de couleur qui tourne (avant d'etre afficher)
    Gère la physique de la voiture

    Attributes
    ----------
    x : float
        Position de la voiture sur l'axe des abscisse (horizontale) en pixels
    y : float
        Position de la voiture sur l'axe des ordonnées (verticale) en pixels
    speed : float
        Vitesse de la voiture (avance si elle est >0 et recule si <0) (vitesse longitudinale)
    angle : float
        Orientation de la voiture en degrés. ###Direction vers laquelle la voiture est orientée
    sprite : pygame.Surface
        Forme de base / d'origine de la voiture
    velocity_angle : float
        Représente l'angle de la trajectoire (réelle) de le voiture
    steering : int
        Direction du "volant" commande du joueur (Ne tourne pas = 0, Tourne à gauche = -1, Tourne à droite = 1)
    drift_intensity : float
        Indique l'intensité du drift (facteur de vitesse * |steering|)
    drifting : bool
        Indique si la voiture dérape ou pas
    """

    def __init__(self, start_col: int, start_row: int, couleur):
        """
        Création d'une voiture au centre d'une case de la grille.

        Parameters
        ----------
        start_col : int
            Numéro de la colonne de départ
        start_row : int
            Numéro de la ligne de départ
        couleur : tuple of int, optional
            Couleur de la voiture en RGB
        """
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0 #indique à quelle vitesse la voiture avance ou recule, mais pas la direction dans laquelle elle se déplace sur l'écran.
        self.angle: float = 0.0 #représente toujours la direction vers laquelle la voiture pointe, même si elle est en train de glisser latéralement.
        self.sprite = self.build_sprite(couleur)
        #Param pr le drift
        self.velocity_angle: float = 0.0 #Direction dans laquelle la voiture se déplace réellement
        self.steering : int = 0 #Direction du volant, gauche, droite ou neutre
        self.drift_intensity: float = 0.0  #Intensité du drift
        self.drifting = False

        #details de la voiture durant la course
        self.progress = None  #variable demander dans block.py par jsp qui
        self.boost_timer = 0        # frames de boost restantes
        self.boost_strength = 0.0   # vitesse ajoutée à chaque frame de boost

    def accelerate(self) -> None:
        """
        Augmente la vitesse de la voiture de "CAR_ACCELERATION"
        """
        self.speed += CAR_ACCELERATION

    #implement deceleration and reverse methods
    def decelerate(self) -> None:
        """
        Diminue la vitesse de la voiture de "CAR_DECELERATION"
        """
        self.speed -= CAR_DECELERATION

    # Implémentation des virages : Tourner à droite/gauche
    def turn(self, direction: int) -> None:
        """
        Méthode permettant de faire tourner la voiture.
        l'angle de la voiture change en fonction de la direction (gauche : 1 et droite : -1) 
        à la même vitesse que accel et decel
        consigne : Tourner à gauche : augmente l’angle de braquage et Tourner à droite : diminue l’angle
        """
        if self.speed > 0.1:
            self.angle += direction #* CAR_TURN_SPEED
        elif self.speed < -0.1:
            self.angle -= direction #* CAR_TURN_SPEED
        
        """ Code de base fonctionne tres bien avec Drive mais pas Reverse
        if self.speed != 0 : # Pour éviter de tourner sur place
        self.angle += direction #* CAR_TURN_SPEED # gauche => direction = +1 et droite => direction = -1
        """

    def update_position(self) -> None:
        """
        Met à jour la position de la voiture en fonction de sa vitesse et de son angle

        Conversion de l'angle en radians car "math.sin" et "math.cos" prennent des rad en arguments.
        Le déplacement de la voiture (frame "speed") est projeté sur 2 axes "x" et "y"
        """
        #self.y += self.speed #code original par défaut
        #modif de update_position pour pouvoir faire tourner la voiture
        rad = math.radians(self.angle) #Pour le drift, on remplace self.angle par self.velocity_angle
        self.x -= math.sin(rad)* self.speed
        self.y -= math.cos(rad)* self.speed

    def build_sprite(self, couleur) -> pygame.Surface:
        """
        Construction de forme/ l'image de la voiture.
        Un rectangle avec les bords arrondis.

        Parameters
        ----------
        couleur : tuple of int
            Couleur du rectangle (RGB)

        Returns
        -------
        surf : pygame.Surface
            une surface de dimension "CAR_WIDTH"*"CAR_HEIGHT"
        """
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, couleur, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        
        # Pare-brise : couleur éclaircie, placé sur l'avant de la voiture
        pare_brise = tuple(min(255, c + 80) for c in couleur)
        pygame.draw.rect(surf, pare_brise,
                (2, 2, CAR_WIDTH - 4,
                 CAR_HEIGHT // 4), border_radius=3)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """
        Revoie le sprite tourné par rapport à un angle "angle" et le rectangle d'affichage

        Returns
        -------
        rotated : pygame.Surface
            Image de la voiture tournée de "-angle" degrés
        rect : pygame.Rect
            Rectangle de la taille de "rotated", centré sur "x,y"
        """
        rotated = pygame.transform.rotate(self.sprite, self.angle) # rotate an image rotate(surface, angle) -> Surface. Unfiltered counterclockwise rotation. The angle argument represents degrees and can be any floating point value. Negative angle amounts will rotate clockwise.
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    def apply_boost(self, strength: float, duration: int) -> None:
        """
        Lance un boost (appelée par un bloc 'B').

        Parameters
        ----------
        strength : float
            Vitesse ajoutée à chaque frame pendant le boost.
        duration : int
            Durée du boost en frames (60 frames = 1 seconde).
        """
        self.boost_strength = strength
        self.boost_timer = duration

    def update_boost(self) -> None:
        """
        Applique le boost pendant une frame, s'il est actif.
        La vitesse augmente sans dépasser 1,5 fois la vitesse maximale.
        """
        if self.boost_timer > 0:
            if self.speed < MAX_SPEED * 1.5:
                self.speed += self.boost_strength
            self.boost_timer -= 1

    def respawn(self) -> None:
        """
        Téléporte la voiture à son dernier point de passage, avec une vitesse nulle.
        Appelée quand la voiture tombe dans le vide ou sort de la carte.
        """
        joueur = self.progress                 # le joueur de cette voiture
        self.x, self.y = joueur.last_checkpoint
        self.speed = 0.0
        self.velocity_angle = self.angle
        self.drifting = False
        self.boost_timer = 0