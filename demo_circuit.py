"""Démo autonome de la partie "Terrains et circuits".

Affiche les circuits du dossier `circuits/`.
    Flèches gauche / droite : changer de circuit
    Échap                   : quitter
"""
import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_TEXT
from model.circuit import Circuit
from view.circuit_renderer import CircuitRenderer


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Démo circuits")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)

    files = Circuit.list_files()
    index = 0
    circuit = Circuit.from_file(files[index])
    renderer = CircuitRenderer()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    step = 1 if event.key == pygame.K_RIGHT else -1
                    index = (index + step) % len(files)
                    circuit = Circuit.from_file(files[index])

        renderer.draw(screen, circuit)
        info = (f"{circuit.name} - {circuit.nb_laps} tours - "
                f"{circuit.nb_checkpoints} points de passage")
        text = font.render(info, True, COLOR_TEXT)
        pygame.draw.rect(screen, (0, 0, 0), text.get_rect(topleft=(8, 8)).inflate(12, 8))
        screen.blit(text, (8, 8))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
