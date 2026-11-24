import pygame
import math
from constants import (CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, CAR_TURN_SPEED)



class Car:
    """
    Voiture de course.
    La classe definie les positions x et y de la voiture.
    Elle définie sa vitesse et son angle de braquage en degrés.
    Elle à un sprite : rectangle de couleur qui tourne (avant d'etre afficher)

    Attributes
    ----------
    x : float
        Position de la voiture sur l'axe des abscisse (horizontale) en pixels
    y : float
        Position de la voiture sur l'axe des ordonnées (verticale) en pixels
    speed : float
        Vitesse de la voiture (avance si elle est >0 et recule si <0)
    angle : float
        Orientation de la voiture en degrés
    sprite : pygame.Surface
        Forme de base / d'origine de la voiture
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
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite(couleur)

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
        #if self.speed != 0 : # Pour éviter de tourner sur place
        self.angle += direction #* CAR_TURN_SPEED # gauche => direction = +1 et droite => direction = -1

    def update_position(self) -> None:
        """
        Met à jour la position de la voiture en fonction de sa vitesse et de son angle

        Conversion de l'angle en radians car "math.sin" et "math.cos" prennent des rad en arguments.
        Le déplacement de la voiture (frame "speed") est projeté sur 2 axes "x" et "y"
        """
        #self.y += self.speed #code original par défaut
        #modif de update_position pour pouvoir faire tourner la voiture
        rad = math.radians(self.angle)
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
