from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.joueur import Joueur
from model.course import Course

"""Contient état du menu, circuit sélectionné, voitures et course en cours.
    car_rouge est la voiture du joueur 1, car_bleue est la voiture du joueur 2
    self.car est la voiture du joueur 1 (a remplacer par self.cars[0] pour le joueur 1 et self.cars[1] pour le joueur 2 
    pour la commande des joueurs, mais pour l'instant on laisse self.car pour le joueur 1)
    self.cars est la liste des voitures, contenant car_rouge et car_bleue

    self.circuit est le circuit sélectionné
    self.state est l'état du jeu (menu, course, etc.)
    self.index_selection est l'index du circuit sélectionné dans la liste des circuits

    self.noms_circuits est la liste des noms des circuits fictifs, à remplacer par une liste de circuits réels une fois on a circuit.txt

    self.load_circuit() charge le circuit sélectionné et spawn les voitures
    self.update() met à jour la position des voitures si l'état est RACING et le circuit est chargé
    self.circuit_suivant() et self.circuit_precedent() permettent de changer le circuit sélectionné dans le menu
    self.spawn_car() crée les deux voitures

"""


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None # circuit actuellement chargé
        self.car: Car | None = None
        self.cars: list[Car] = []
        self.noms_circuits = ["Prairie", "Glacier", "Canyon"] # Le nom des circuits qui va s'afficher sur le menu
        self.index_selection: int = 0 #indice du circuit sélectionné dans la liste des circuits 
        
        self.joueurs = []     # joueurs 1 et 2
        self.race = None      # course en cours


    def circuit_suivant(self) -> None:
        """Sélectionne le circuit suivant (revient au premier après le dernier)."""
        if self.index_selection < len(self.noms_circuits) - 1: #eviter l'index out of range
            self.index_selection += 1
        else:
            self.index_selection = 0

    def circuit_precedent(self) -> None:
        """Sélectionne le circuit précédent (va au dernier avant le premier)."""
        if self.index_selection > 0: #eviter l'index out of range
            self.index_selection -= 1
        else:
            self.index_selection = len(self.noms_circuits) - 1

    def load_circuit(self) -> None:
       """Charge le circuit choisi dans le menu depuis le dossier circuits/,
        puis place les voitures.
        """
       fichiers = Circuit.list_files() # les fichiers .txt du dossier circuits
       fichier = fichiers[self.index_selection] # celui choisi dans le menu
       self.circuit= Circuit.from_file(fichier)# lit le fichier et crée les cases
       self.spawn_car()
       self.race = Course(self.circuit, self.joueurs)


    def spawn_car(self) -> None:
        """Crée les deux voitures sur les blocs de départ 1 et 2 du circuit.
        
        """
        circuit = self.circuit                   # le circuit chargé
        departs = circuit.starts                 # cases de départ : {1: (col, row), 2: (col, row)}
        angle = circuit.start_angle - 90      # direction de départ des voitures (coupable à trouver : Angle pas match, soit car ou circuit fautif)
        #faut trouver qui à mis son angle 0 à droite

        col, row = departs[1]                    # case du bloc 1
        car_rouge = Car(col, row, (255, 0, 0))   # voiture du joueur 1
        car_rouge.angle = angle

        col, row = departs[2]                    # case du bloc 2
        car_bleue = Car(col, row, (0, 0, 255))   # voiture du joueur 2
        car_bleue.angle = angle

        self.cars = [car_rouge, car_bleue]
        self.car = car_rouge

        # Un joueur par voiture ; sa case de départ est son premier point de réapparition
        joueur1 = Joueur(1, car_rouge, (car_rouge.x, car_rouge.y))
        joueur2 = Joueur(2, car_bleue, (car_bleue.x, car_bleue.y))
        self.joueurs = [joueur1, joueur2]

    def update(self) -> None:
        """Avance le jeu d'une frame, déplace les voitures, puis applique
        les effets des cases (boost, vide, points de passage, arrivée)."""
        if self.state != GameState.RACING or self.race is None:
            return
        for car in self.cars:
            car.update_position()
            car.update_boost()
        self.race.update()
        if self.race.winner: #un joueur à terminer tous les tours
            self.state = GameState.FINISHED

    def retour_menu(self) -> None:
        """Termine la course et revient au menu principal."""
        self.state = GameState.MENU
        self.course = None