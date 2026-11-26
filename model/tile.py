"""Case du circuit : un terrain, plus éventuellement un bloc."""
import random

import pygame

from constants import TILE_SIZE
from model.terrain import Terrain, Void
from model.block import Block


class Tile:
    """Case de la grille du circuit.

    Remplace la classe `RoadTile` du code de départ : une case a maintenant
    un terrain (obligatoire) et peut porter un bloc (facultatif).

    Attributes
    ----------
    col : int
        Colonne de la case dans la grille.
    row : int
        Ligne de la case dans la grille.
    terrain : Terrain
        Terrain de la case.
    block : Block | None
        Bloc posé sur la case, ou None.
    sprite : pygame.Surface | None
        Image de la case (mise en cache après le premier dessin).
    """

    def __init__(self, col: int, row: int, terrain: Terrain,
                 block: Block | None = None):
        """
        Parameters
        ----------
        col : int
            Colonne de la case.
        row : int
            Ligne de la case.
        terrain : Terrain
            Terrain de la case.
        block : Block | None
            Bloc de la case (None par défaut).
        """
        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Retourne l'image de la case (terrain uniquement, sans le bloc).

        L'image est construite une seule fois puis réutilisée. Quelques
        points plus sombres, placés de façon reproductible, donnent un peu
        de texture au terrain.

        Parameters
        ----------
        tile_size : int
            Côté de la case en pixels.

        Returns
        -------
        pygame.Surface
            L'image de la case.
        """
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite

        color = self.terrain.get_color()
        dark = tuple(max(0, c - 20) for c in color)

        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(color)

        # Le générateur est initialisé avec la position : la texture est
        # toujours la même pour une case donnée.
        generator = random.Random(self.col * 1000 + self.row)
        for _ in range(8):
            x = generator.randint(0, tile_size - 4)
            y = generator.randint(0, tile_size - 4)
            pygame.draw.rect(surface, dark, (x, y, 4, 4))

        pygame.draw.rect(surface, dark, surface.get_rect(), 1)

        self.sprite = surface
        return self.sprite

    def get_center(self) -> tuple[float, float]:
        """Retourne le centre de la case en pixels.

        Returns
        -------
        tuple[float, float]
            Coordonnées (x, y) du centre.
        """
        return (self.col * TILE_SIZE + TILE_SIZE / 2,
                self.row * TILE_SIZE + TILE_SIZE / 2)

    def is_void(self) -> bool:
        """Indique si le terrain de la case est du vide."""
        return isinstance(self.terrain, Void)

    def on_car_enter(self, car, circuit) -> None:
        """Applique les effets de la case à une voiture qui s'y trouve.

        Le terrain agit en premier (ex : le vide téléporte la voiture),
        puis le bloc s'il y en a un.

        Parameters
        ----------
        car : Car
            La voiture présente sur la case.
        circuit : Circuit
            Le circuit en cours.
        """
        self.terrain.on_car_enter(car)
        if self.block is not None:
            self.block.on_car_enter(car, circuit)
