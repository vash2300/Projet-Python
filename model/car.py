import pygame
import math
from constants import (CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, CAR_TURN_SPEED)



class Car:

    def __init__(self, start_col: int, start_row: int, couleur):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite(couleur)

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def update_position(self) -> None:
        #self.y += self.speed #code original par défaut
        #modif de update_position pour pouvoir faire tourner la voiture
        rad = math.radians(self.angle)
        self.x += math.sin(rad)* self.speed
        self.y += math.cos(rad)* self.speed

    def build_sprite(self, couleur) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, couleur, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    #implement deceleration and reverse methods
    def decelerate(self) -> None:
        self.speed -= CAR_DECELERATION

    # Implémentation des virages : Tourner à droite/gauche
    def turn(self, direction: int) -> None:
        """
        Méthode permettant de faire tourner la voiture.
        l'angle de la voiture change en fonction de la direction (droite : 1 et gauche : -1) 
        à la même vitesse que accel et decel
        """
        if self.speed != 0 :
            self.angle += direction * CAR_TURN_SPEED
