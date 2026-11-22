"""Contient les étapes de main.py et fait le lien entre les différentes parties du MVC """
import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """
    Controleur du jeu

    La class gère les événements clavier, transmet les commandes du joueur au modèle, 
    organise la mise à jour du jeu et demande à la vue d'actualiser l'affichage.

    Atributes
    ---------
    screen : pygame.Surface
        Initialize a window or screen for display. This function will create a display Surface (pygame documentation)
    clock : pygame.Clock
        Creates a new Clock object that can be used to track an amount of time (pygame documentation)
    model : GameModel
        Class qui initialise/contient l'état, le circuit e la voiture
    view : GameView
        class qui initialise/contient la vue de la fenètre du jeu
    input_handler : Inputhandler
        Class qui gère les entrées clavier (inputs des joueurs)
    running : bool
        verifie si l'initialisation à été déclanchée
    """

    def __init__(self):
        """
        Initialise le contrôleur et ses différents composants.
        Crée la fenêtre du jeu, l'horloge et les instances du modèle,
        de la vue et du gestionnaire des entrées clavier.
        """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """
        Méthode utlilisé dans la boucle principale du jeu
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """
        Traite les évenements pygame.
        Gère la fermeture de la fenètre.
        Gère les evènements liés à l'appui d'une touche.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """
        Traite une touche du clavier selon l'état actuel du jeu

        Parameters
        ----------
        key : int
            Touche appuyée en code pygame
        """
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECT:
            self.handle_select_key(key)

    def handle_menu_key(self, key: int) -> None:
        """
        Gère les commandes clavier disponibles dans le menu.

        La touche Entrée permet de charger le circuit et de démarrer
        la course. La touche Échap permet de quitter le jeu.

        Parameters
        ----------
        key : int
            Code Pygame correspondant à la touche pressée.
        """
        """"
        if key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        """
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECT #selection du circuit sur le menu
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_select_key(self, key: int) -> None:
        """Choix du circuit : flèches pour changer, Entrée pour jouer,
        Échap pour revenir au menu."""
        if key == pygame.K_UP:
            self.model.circuit_precedent()
        elif key == pygame.K_DOWN:
            self.model.circuit_suivant()
        elif key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """
        C'est une mise à jour de l'état du du jeu.
        
        La fonction vérifie que le jeu est en mode RACING.
        Elle récupère les entrées du joueur (input_handler.get_inputs()), les applique à la voiture (apply_input()).
        Elle demande au modèle de mettre à jour la pos (model.update())
        """
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car
        self.apply_input(car, p1_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """
        Applique les commandes du joueur à la voiture correspondante.

        parameters
        ----------
            car : Car
                Class Car, la voiture controlable par les joueurs

        """
        if player_input['accelerate']:
            car.accelerate()
        if player_input['decelerate']:
            car.decelerate()

    def render(self) -> None:
        """
        Actualisation de l'affichage. Le model est envoyée à la vue pour pouvoir représenter l'état actuel du jeu
        """
        self.view.draw(self.model)

    def quit(self) -> None:
        """
        Arrêt du jeu et de pygame
        """
        self.running = False
        pygame.quit()
        sys.exit()
