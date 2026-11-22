import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "decelerate",
    pygame.K_LEFT:   "turn_left", # Ajout de la touche fleche gauche
    pygame.K_RIGHT:  "turn_right", # Ajout de la touche flèche droite
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
