"""Affichage du circuit à l'écran (partie Vue du MVC)."""
import pygame

from constants import TILE_SIZE, BLOCK_COLORS
from model.circuit import Circuit
from model.tile import Tile


class CircuitRenderer:
    """Dessine un circuit : terrains puis symboles des blocs.

    Le circuit ne change pas pendant la course. Il est donc dessiné une seule
    fois sur une grande image (`background`), qui est ensuite simplement
    recopiée à l'écran à chaque frame.

    Attributes
    ----------
    font : pygame.font.Font
        Police des symboles de blocs.
    background : pygame.Surface | None
        Image du circuit complet.
    cached_circuit : Circuit | None
        Circuit correspondant à `background`.
    """

    def __init__(self):
        """Crée la police. pygame.init() doit avoir été appelé avant."""
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.background: pygame.Surface | None = None
        self.cached_circuit: Circuit | None = None

    def draw(self, screen: pygame.Surface, circuit: Circuit) -> None:
        """Dessine le circuit à l'écran.

        L'image est reconstruite uniquement si le circuit a changé.

        Parameters
        ----------
        screen : pygame.Surface
            Surface sur laquelle dessiner.
        circuit : Circuit
            Circuit à afficher.
        """
        if circuit is not self.cached_circuit:
            self.__build_background(circuit)
        screen.blit(self.background, (0, 0))

    def __build_background(self, circuit: Circuit) -> None:
        """Construit l'image complète du circuit (terrains + blocs)."""
        surface = pygame.Surface((circuit.pixel_width(),
                                  circuit.pixel_height()))
        for row in circuit.grid:
            for tile in row:
                position = (tile.col * TILE_SIZE, tile.row * TILE_SIZE)
                surface.blit(tile.get_sprite(TILE_SIZE), position)
                if tile.block is not None:
                    self.__draw_block_symbol(surface, tile)

        self.background = surface
        self.cached_circuit = circuit

    def __draw_block_symbol(self, surface: pygame.Surface,
                            tile: Tile) -> None:
        """Dessine le symbole du bloc (pastille colorée + lettre)."""
        label = tile.block.label
        color = BLOCK_COLORS.get(label, (255, 255, 255))
        center_x, center_y = tile.get_center()
        center = (int(center_x), int(center_y))
        radius = TILE_SIZE // 3

        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, (20, 20, 20), center, radius, 2)
        text = self.font.render(label, True, (20, 20, 20))
        surface.blit(text, text.get_rect(center=center))
