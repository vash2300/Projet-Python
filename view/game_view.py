import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel
from view.circuit_renderer import CircuitRenderer
from model.course import Course


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.circuit_renderer = CircuitRenderer()   # dessine le circuit(terrains + blocs)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.CIRCUIT_SELECT:
            self._draw_select(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
            self._draw_tours(model)
        elif model.state == GameState.FINISHED:
            self._draw_racing(model)
            self._draw_victoire(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))


    #utilisation de la fonction _draw_select pour dessiner l'écran de sélection du circuit
    def _draw_select(self, model: GameModel) -> None:
        """Écran de choix du circuit : un bouton par circuit,
        le circuit sélectionné est mis en évidence."""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render("Choix du circuit", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        for i, nom in enumerate(model.noms_circuits):
            y = 300 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            selectionne = (i == model.index_selection) # circuit sélectionné
            couleur = COLOR_ACCENT if selectionne else COLOR_TEXT
            bordure = COLOR_ACCENT if selectionne else COLOR_PANEL_BORDER
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, bordure, rect, 2, border_radius=8)
            text_surf = self.font.render(nom, True, couleur)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        aide = self.font.render("Haut/Bas : choisir   Entrée : jouer   Échap : retour",True, COLOR_TEXT) #instructions pour l'utilisateur
        self.screen.blit(aide, aide.get_rect(center=(cx, 700))) #affichage des instructions en bas de l'écran

    def _draw_racing(self, model: GameModel) -> None:

        if model.circuit is None:
            return
        self.circuit_renderer.draw(self.screen, model.circuit)

        # Dessiner les deux voitures
        for car in model.cars:
            if car.boost_timer > 0:
                self._draw_halo_boost(car)
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)

    def _draw_tours(self, model: GameModel) -> None:
        """affichage d'infos en haut de l'écran contient le nombre de tours de chaque joueur."""
        course = model.race
        for joueur in course.joueurs:
            numero_joueur = joueur.numero

            tour = joueur.laps + 1
            texte = f"J{numero_joueur}   Tour {tour}/{course.nb_laps}"
            texte += f"     Passages {joueur.next_checkpoint}/{course.nb_checkpoints}"

            voiture = joueur.car                # la voiture de ce joueur
            if voiture.boost_timer > 0:         # le boost est actif
                texte += "   BOOST !"           # on ajoute le mot à la fin du texte


            if numero_joueur == 1: #pour le joueur 1
                couleur = (255, 0, 0)
                position = (16, 5)
            else:
                couleur = (0, 0, 255)
                position = (WINDOW_WIDTH - 300, 5)

            voiture = joueur.car
            if voiture.boost_timer > 0:        # le boost est actif
                texte += "   BOOST !"
            image = self.font.render(texte, True, couleur)
            self.screen.blit(image, position)

    def _draw_victoire(self, model: GameModel) -> None:
        """Écran de victoire : nom du gagnant au centre de l'écran"""
        gagnant = model.race.winner          # le Joueur qui a gagné
        numero = gagnant.numero

        # block semi_transparent superposé sur le racing
        shade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 160))
        self.screen.blit(shade, (0, 0))

        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        # Cadre derrière le message
        cadre = pygame.Rect(0, 0, 640, 200)
        cadre.center = (cx, cy)
        pygame.draw.rect(self.screen, COLOR_PANEL, cadre, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, cadre, 3, border_radius=12)

        # Message dans la couleur du gagnant
        if numero == 1:
            couleur = (255, 0, 0)
        else:
            couleur = (0, 0, 255)
        titre = self.font.render(f"Joueur {numero} gagne !", True, couleur)
        self.screen.blit(titre, titre.get_rect(center=(cx, cy - 30)))

        aide = self.font.render("Entrée : retour au menu", True, COLOR_TEXT)
        self.screen.blit(aide, aide.get_rect(center=(cx, cy + 40)))

    def _draw_halo_boost(self,car) -> None:
        """Dessine un halo jaune semi-transparent sous une voiture boostée.
        car : Voiture dont le boost est actif.
        """
        rayon = 30                                  # un peu plus grand que la voiture
        taille = rayon * 2

        # Feuille transparente juste assez grande pour le cercle
        halo = pygame.Surface((taille, taille), pygame.SRCALPHA)
        pygame.draw.circle(halo, (255, 255, 0, 110), (rayon, rayon), rayon)

        # blit place le coin haut-gauche, on recule d'un rayon pour centrer sur la voiture
        x = int(car.x) - rayon
        y = int(car.y) - rayon
        self.screen.blit(halo, (x, y))
        