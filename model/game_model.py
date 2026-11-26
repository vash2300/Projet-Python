from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile

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

        #a modifier les 2 apres la fonctionalite bloc implementer
        self.n_tours = 3              # nombre de tours pour gagner
        self.tours = [0, 0]           # tours terminés : [joueur 1, joueur 2]


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

    def spawn_car(self) -> None:
        """Crée les deux voitures côte à côte.
        self.car reste la voiture du joueur 1, car le contrôleur l'utilise encore
        self.cars contient les deux voitures.
        car(positionX, positionY, couleur) : positionX et positionY sont les coordonnées de la voiture sur la grille, couleur est un tuple RGB
        """

        #a remplacer par la position de départ du circuit, ici c'est juste un exemple
        car_rouge = Car(7,1,(255,0,0)) # couleur de la voiture du joueur 1
        car_bleue = Car(8, 1,(0,0,255)) # couleur de la voiture du joueur 2
        self.cars = [car_rouge, car_bleue] #list qui contient les deux voitures, la voiture du joueur 1 et la voiture du joueur 2

        self.car = car_rouge #a retirer apres avoir implementé la commande du joueur 2, ici pour ne pas avoir d'erreur, on laisse l'exemple voiture 1

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
